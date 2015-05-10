#!/usr/bin/env python

import socket  
from collections import defaultdict





d=[]
def create_global_vlan():
    global d
    d.append({'0':['None']})
    res=defaultdict(list)
    for i in range (1,17):
        res=createVlanId(i)
        d.append(res)
    
def same_pod(host,i,lst):
    for pod in lst:
        if host in pod:
            if i in pod:
                return True
    return False

def createVlanId(host): 
        hostpair=[[1,2],[3,4],[5,6],[7,8],[9,10],[11,12],[13,14],[15,16]]
        samepod=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        dest=[]
        vid = 0
        res=''
        for i in range (1,17):
            if (i!= host):
                vid = (i << 4)+ host
                if ([host,i] in hostpair or [i,host] in hostpair):
                    temp=(i,vid*10+1)
                    dest.append(temp)
                elif (same_pod(host,i,samepod)):
                    temp=(i,vid*10+1)
                    dest.append(temp)
                    temp=(i,vid*10+2)
                    dest.append(temp)
                else:
                    temp=(i,vid*10+1)
                    dest.append(temp)
                    temp=(i,vid*10+2)
                    dest.append(temp)
                    temp=(i,vid*10+3)
                    dest.append(temp)
                    temp=(i,vid*10+4)
                    dest.append(temp)
        d=defaultdict(list)
        for host,vlan in dest:
            d[host].append(vlan)
        return d

def assign_vlan(data, addr):
    global d
    dest = int(data.split()[1])
    demand=int(data.split()[2])
    res=''
    result='assign'
    print dest
    print addr
    source=int(addr[0].split(".")[3])
    print source
    total_route=d[dest].items()
    print "total route", total_route
    vlan_list=total_route[source-1][1]
    print "vlan list", vlan_list, len(vlan_list)
    if len(vlan_list)>demand:
        #print "in 1"
        for i in range (0,demand):
            res=res+" "+str(vlan_list[i])
        for id in res:
            vlan_list.remove(id)
        d[dest][source]=vlan_list
        result=result+" "+str(res)
        #print "res", res
    elif len(vlan_list)<=demand and len(vlan_list) is not 0:
        #print "in 2"
        for i in vlan_list:
            res=res+" "+str(i)
        vlan_list=[]
        d[dest][source]=vlan_list
        result=result+" "+str(res)
        #print "res", res
    elif len(vlan_list) is 0:
        #print "in 3"
        result="NA"
    #print "result", result
    return result

def release_vlan(data,addr):
    global d
    dest = int(data.split()[1])
    source=int(addr[0].split(".")[3])
    vlan_list=data.split()[2].split(",")
    curr_list=d[dest][source]
    for id in vlan_list[:len(vlan_list)-1]:
        curr_list.append(int(id))
    d[dest][source]=curr_list
    #print "After Release", d[dest]

def main():
    global d
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    host = socket.gethostname()
    port=5000
    arbiter_ip='20.0.0.100'
    s.bind((arbiter_ip,port))
    s.listen(15)
    create_global_vlan()
    #print "vlan list", d
    while True:
        #print "waiting for request"
        conn, addr = s.accept()
        data=conn.recv(1024)
        #print "request from host", addr
        #print "request:", data
        type=data.split()[0]
        if type == 'demand':
            send_data=assign_vlan(data, addr)
            conn.send(send_data)
            conn.close()
        if type == 'done':
            release_vlan(data, addr)
            conn.close()
if __name__=="__main__":
    main()
        