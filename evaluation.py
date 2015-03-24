import os
from scapy.all import *
import re
import time

num_host = 16

g_start_time = time.time()

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

    pkttrace = rdpcap(dump_file)
    for pkt in pkttrace:
        #print pkt.time
        #exit(1)
        
        if pkt.haslayer(IP) == 0 or  pkt.haslayer(UDP) == 0:
            continue


        src = pkt.getlayer(IP).src
        dst = pkt.getlayer(IP).dst
        if dst != hostip:
            continue
            
        dport = pkt.getlayer(IP).dport
        key = str(src)+':'+str(dst)+':'+str(dport)
        ts = pkt.time
        
        if key not in spec:
            continue
            

        if key not in g_stat:
            g_stat[key] = {}
            
        # suppose you have only ONE 802.1Q layer
        if pkt.haslayer(Dot1Q):
            vlan = int(pkt.getlayer(Dot1Q).vlan)
            #print vlan

        if vlan not in g_stat[key]:
            g_stat[key][vlan] = (0,ts)
            
        header_size = 20 # IP header
        if pkt.proto == 17 or pkt.proto == 6:
            header_size += 8  # L4 header

            
        g_stat[key][vlan] = (g_stat[key][vlan][0] + (pkt.len - header_size), ts)


def stat_summary(spec):
    global g_stat
    
    for key in spec:
        if key not in g_stat:
            print "flow: " + key + " Missing"
            g_correctness_list.append(0)
            continue
        flowsize = 0
        finish_time = 0
        for vlan in g_stat[key]:
            #print stat[key][vlan]
            flowsize += g_stat[key][vlan][0]
            
            if g_stat[key][vlan][1] > finish_time:
                finish_time = g_stat[key][vlan][1]
            #test
            #print "vlan: " + key+'\t'+ str(vlan) + '\t' + str(stat[key][vlan])
        if spec[key] == flowsize:
            result = "OK"
            g_correctness_list.append(1)
        else:
            result = "Wrong flow size"
            g_correctness_list.append(0)

        FCT = finish_time - g_start_time
        throughput = flowsize * 8.0 / (FCT)/ 1e6
    
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
        
    for hostid in range(1,num_host+1):
        host = 'h' + str(hostid)
        hostip = '10.0.0.'+str(hostid)
        tracefile = 'dump/' + host + '.pcap'
        get_dump_stat(tracefile, traffic, hostip)

        
    #analyze the traffic statistics
    stat_summary(traffic)
    
    #print overall result
    print "=== Overall result ==="
    print "correct flows: " + str(sum(g_correctness_list))
    print "total flows: " + str(len(g_correctness_list))
    if len(g_throughput_list) == 0:
        print "ave throughput: N/A"
    else:
        print "ave throughput: " + str(sum(g_throughput_list)/len(g_throughput_list))
    if len(g_FCT_list) == 0:
        print "tail FCT: N/A"
    else:
        print "tail FCT: " + str(min(g_FCT_list))
    

    
def kill_all_task():
    cmd = "ps -ef | grep \'tcpdump\|cperf\' | grep -v grep | awk \'{print $2}\'"
    pids = os.popen(cmd).read()
    pid_all = ""
    strs = pids.split('\n')
    for pid in strs:
        pid_all += str(pid)
        pid_all += " "
    #print pid_all
    os.system("sudo kill " + pid_all)

if __name__=='__main__':

    print "Starting Arbiter..."
    cmd = "./arbiter"
    os.system(cmd)
    
    print "Starting tcpdump..."
    time.sleep(1)
    for hostid in range(1,num_host+1): 
        host = 'h' + str(hostid)
        cmd = 'mininet/util/m ' + host + ' sudo tcpdump -i ' + host +'-eth0' + ' -n -s 64 portrange 5000-5005 -w dump/' + host + '.pcap &'
        print cmd
        os.system(cmd)

    print "Starting traffic..."
    time.sleep(1)
    for hostid in range(1,num_host+1): 
        host = 'h' + str(hostid)
        cmd = 'mininet/util/m ' + host + ' ./cperf trace/' + host + '.tr &'
        print cmd
        os.system(cmd)

    #sleep sufficient amount of time
    #change the value in need
    time.sleep(60)

    print "Terminating all task..."
    kill_all_task()

    print "Analyzing traffic statistics..."
    dump_trace_analysis()
