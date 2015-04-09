import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import os
from scapy.all import *
import re
import time
import shutil
from datetime import datetime

#
num_host = 16

#g_start_time = time.localtime()
g_start_time = datetime.now()

g_correctness_list = []
g_throughput_list = []
g_FCT_list = []
g_stat = {}

def traffic_spec(host,hostip):
    traffic = {}
    p = re.compile("-d h(\S*) -p (\S*) -n (\S*)")
    traffic_file = 'traffic/' + host +'.tr'
    for line in open(traffic_file):
        m = p.match(line)
        if m != None:
            dstid = m.group(1)
            dstport = m.group(2)
            vol = m.group(3)
            vol_num = int(re.findall("\d+", vol)[0])
            if 'K' in vol:
                vol_num *= 1000
            elif 'G' in vol:
                vol_num *= 1e9
            elif 'M' in vol:
                vol_num *= 1e6
            traffic[hostip+':'+'10.0.0.'+dstid+':'+dstport] = vol_num
    return traffic


    
#compare dump file with traffic spec
def get_dump_stat(dump_file, spec, hostip):
    #global g_throughput_list
    #global g_FCT_list
    #global g_correctness_list
    global g_stat
    global g_start_time
    
    p = re.compile("(\S*)\:(\S*)\:(\S*)")
    for flow in spec: 
        m = p.match(flow)
        if m != None:
            src = m.group(1)
            dst = m.group(2)
            port = m.group(3)
            #print src,dst,port
            #print dst,hostip
            if dst == hostip:
                print "Analyzing trace for flow: " + src + " -> " + dst +":"+port
                #if (os.path.exists(dump_file) == False):
                #    print dumpfile + ' does not exists'
                #    exit(1)
                
                cmd = 'sudo tcpdump vlan and dst ' + dst + ' and src ' + src + ' and dst port ' + port + ' -r ' + dump_file + ' -w dump/tmp.pcap > /dev/null 2>&1'
                #print cmd
                os.system(cmd)

                cmd = 'capinfos -Tm dump/tmp.pcap'
                #print cmd
                info = os.popen(cmd).read()
                pos1 = info.find("\n")
                #print info[:pos1]
                pos2 = info.find("\n", pos1+1)
                info_list = info[pos1+1:pos2].split(",")                    
                #print info_list
                pkt = int(info_list[6])
                
                #here we only calculate payload size
                #Ether(14) + Vlantag(4) + IP (20) + UDP(8) = 46 Byte header
                #let us know if this calculation does not work for you
                byt = int(info_list[8]) - pkt * 46  #total bytes
                thr = float(info_list[13])       #bps
                pktrate = float(info_list[15])   #packets/sec
                pktsize = float(info_list[14])   #average packet size
                #print pkt, byt, thr,pktrate, pktsize
               
                
                # the duration in capinfos is not precise
                # instead we use..
                if pkt == 0:
                    g_stat[flow] = (byt, 0)
                else:
                    cmd = 'tshark -r dump/tmp.pcap -Y "frame.number == 1" -T fields -e frame.time'
                    #print cmd
                    start = os.popen(cmd).read()
                    cmd = 'tshark -r dump/tmp.pcap -Y "frame.number == ' + str(pkt) + '\" -T fields -e frame.time'
                    #print cmd
                    end = os.popen(cmd).read()

                    #local time
                    #starttime = datetime.strptime(start.split('.')[0] + '.' + start.split('.')[1][0:6],"%b  %d, %Y %H:%M:%S.%f")
                    endtime = datetime.strptime(end.split('.')[0] + '.' + end.split('.')[1][0:6],"%b  %d, %Y %H:%M:%S.%f")
                    #endtime = time.strptime(end.split('.')[0] + '.' + end.split('.')[1][0:6],"%b  %d, %Y %H:%M:%S.%f")
                    
                    #duration = (endtime-starttime).seconds*1.0 + (endtime-starttime).microseconds * 10.0/1000000
                    #delta = time.mktime(endtime) - time.mktime(g_start_time)
                    #epoch = datetime.utcfromtimestamp(0)
                    delta = (endtime - g_start_time).total_seconds()
                    
                    g_stat[flow] = (byt, delta)
                    
                #exit(1) 

    #return 
    
    #for pkt in pkttrace:
        #print pkt.time
        #exit(1)
        
     #   if pkt.haslayer(IP) == 0 or  pkt.haslayer(UDP) == 0:
     #      continue


     #   src = pkt.getlayer(IP).src
     #   dst = pkt.getlayer(IP).dst
     #   if dst != hostip:
     #       continue
            
        #dport = pkt.getlayer(IP).dport
        #key = str(src)+':'+str(dst)+':'+str(dport)
        #ts = pkt.time
        
        #if key not in spec:
        #    continue
            

        #if key not in g_stat:
        #    g_stat[key] = {}
            
        # suppose you have only ONE 802.1Q layer
        #if pkt.haslayer(Dot1Q):
         #   vlan = int(pkt.getlayer(Dot1Q).vlan)
            #print vlan

        #if vlan not in g_stat[key]:
        #    g_stat[key][vlan] = (0,ts)
            
        #header_size = 20 # IP header
        #if pkt.proto == 17 or pkt.proto == 6:
        #    header_size += 8  # L4 header

            
        #g_stat[key][vlan] = (g_stat[key][vlan][0] + (pkt.len - header_size), ts)


def stat_summary(spec):
    global g_stat
    
    for key in spec:
        if key not in g_stat:
            print "flow: " + key + " Missing"
            g_correctness_list.append(0)
            continue
        flowsize = 0
        finish_time = 0
        #for vlan in g_stat[key]:
            #print stat[key][vlan]
            #flowsize += g_stat[key][vlan][0]
            
            #if g_stat[key][vlan][1] > finish_time:
            #    finish_time = g_stat[key][vlan][1]
            #test
            #print "vlan: " + key+'\t'+ str(vlan) + '\t' + str(stat[key][vlan])
        flowsize = g_stat[key][0]
        finish_time = g_stat[key][1]

        if spec[key] == flowsize:
            result = "OK"
            g_correctness_list.append(1)
            success = 1
        else:
            result = "Wrong flow size"
            g_correctness_list.append(0)
            success = 0

            
        if finish_time != 0 and success == 1:
            #FCT = finish_time - g_start_time
            FCT = finish_time
            throughput = flowsize * 8.0 / (FCT)/ 1e6
        else:
            FCT = float('inf')
            throughput = 0
            
    
        print "flow " + key + '\t' + "FCT " + str(FCT) + '\t' + "thr " + str(throughput) +" Mbps\texpt " + str(spec[key]) + '\t' + "dump " + str(flowsize) + '\t' + result
        
        #save per flow stat
        g_throughput_list.append(throughput)
        g_FCT_list.append(FCT)
		
		
def dump_trace_analysis():
    global g_throughput_list
    global g_FCT_list
    global g_correctness_list

    traffic = {}
    for hostid in range(1,num_host+1):
        host = 'h' + str(hostid)
        hostip = '10.0.0.'+str(hostid)
        # retrieve traffic specification
        traffic_ = traffic_spec(host,hostip)
        for item in traffic_:
            if item not in traffic:
                traffic[item] = traffic_[item]
            else:
                traffic[item] += traffic_[item]

    #print traffic
    
    for hostid in range(1,num_host+1):
        host = 'h' + str(hostid)
        hostip = '10.0.0.'+str(hostid)
        tracefile = 'dump/' + host + '.pcap'
        #print "process dump for ",host
        get_dump_stat(tracefile, traffic, hostip)


    #analyze the traffic statistics
    stat_summary(traffic)
    
    #print overall result
    print "=== Overall result ==="
    print "correct flows: " + str(sum(g_correctness_list))
    print "total flows: " + str(len(g_correctness_list))
    

    if len(g_throughput_list) == 0:
        print "ave throughput: N/A"
        ave_th = 0
    else:
        ave_th = sum(g_throughput_list)/len(g_throughput_list)
        print "ave throughput: " + str(ave_th)
    if len(g_FCT_list) == 0:
        tail_latency = 0
        print "tail FCT: N/A"
    else:
        tail_latency = max(g_FCT_list)
        print "tail FCT: " + str(tail_latency)

    #use it for now
    ave_size = 50
    score = (ave_th / 1000 + ave_size * 8 / 1000 / tail_latency) * 100
    print "score: ",score

    
def kill_all_task():
    _digit = re.compile('\d')
    cmd = "ps -ef | grep \'tcpdump\' | grep -v grep | awk \'{print $2}\'"
    pids = os.popen(cmd).read()
    pid_all = ""
    strs = pids.split('\n')
    for pid in strs:
        pid_all += str(pid)
        pid_all += " "
        
    #print "pid", pid_all
    if bool(_digit.search(pid_all)):
        os.system("sudo kill " + pid_all)

    
    cmd = "ps -ef | grep \'cperf\|./arbiter\' | grep -v grep | grep -v network | awk \'{print $2}\'"
    pids = os.popen(cmd).read()
    pid_all = ""
    strs = pids.split('\n')
    for pid in strs:
        pid_all += str(pid)
        pid_all += " "
    #print "pid",pid_all
    if bool(_digit.search(pid_all)):
        os.system("sudo kill -9 " + pid_all)


if __name__=='__main__':

    print "Clear existing task..."
    kill_all_task()

    if os.path.exists("dump"):
        shutil.rmtree('dump')

    if os.path.exists("logs"):
        shutil.rmtree('logs')

    if not os.path.exists("dump"):
        os.makedirs("dump")
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    print "Starting Arbiter..."
    cmd = "./arbiter >logs/arbiter.log 2>&1 &"
    print cmd
    os.system(cmd)
    
    print "Starting tcpdump..."
    time.sleep(1)
    for hostid in range(1,num_host+1): 
        host = 'h' + str(hostid)
        cmd = '~/mininet/util/m ' + host + ' sudo tcpdump -i ' + host +'-eth0' + ' -n -s 64 -B 8192 -w dump/' + host + '.pcap >/dev/null 2>&1 &'
        print cmd
        os.system(cmd)

    print "Starting traffic..."
    time.sleep(1)
    for hostid in range(1,num_host+1): 
        host = 'h' + str(hostid)
        cmd = '~/mininet/util/m ' + host + ' ./cperf traffic/' + host + '.tr > logs/cperf-' + host +'.log 2>&1 &'
        print cmd
        os.system(cmd)

    #sleep sufficient amount of time
    #change the value in need
    print "wait 300 seconds for all flows finished..."
    time.sleep(300)

    print "Terminating all task..."
    kill_all_task()

    print "Analyzing traffic statistics..."
    dump_trace_analysis()

    
