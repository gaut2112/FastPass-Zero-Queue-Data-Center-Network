#!/usr/bin/env python
import sys
import socket  
from collections import defaultdict
import socket
import time
import threading
import ctypes
import os





vlan=[0,321,482,641,802,961,1122,1281,1442,1601,1762,1921,2082,2241,2402,2561]
def send_packets(src, dest, port):
    global vlan
    v=vlan[src]
    #print v
    pth = str(os.getcwd())+"/library.so"
    for i in xrange (50):
        ctypes.CDLL(pth).sendPacket(v,1000,dest,src,port)
        
def client_agent(req, src):
    arbiter_ip='20.0.0.100'
    allocation=''
    i=0
    prt=5000
    alloc=''
    for re in req:
        i=i+1
        dest=0
        port=0
        demand_str='demand'
        traffic_req=re.split()
        dest=int(traffic_req[1][1:])
        port=int(traffic_req[3])
        demand_str=demand_str+" "+str(dest)+" 4"
        #print demand_str
        def send_receive_demand(demand):
            #print "in send recieve demand"
            host = socket.gethostname()
            alloc=''
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)         # Create a socket object# Get local machine name
            s.connect((arbiter_ip, prt))
            s.send(demand)
            alloc=s.recv(1024)
            return alloc
        allocation=send_receive_demand(demand_str)
        #print "allocation:"+allocation
        send_packets(src, dest, port)
        #release_vlan(allocation)
        #t =threading.Thread(name="Req"+str(i),target=send_demand(req, receive_demand))
        #def receive_demand(s):
        #    allocation=''
        #    allocation=s.recv()
        #    return allocation
        #if 'assign' in alloc:
        #    send_packets(alloc)
        #elif 'NA' in alloc:
        #    backlog.append(re)

def command_parser(inputfile):
    #print inputfile
    fin=[]
    f = open(inputfile)
    fi=f.read().splitlines()
    
    for i in fi:
        if (i.find('d') != -1):
            fin.append(i)
    #print "file:",fin
    if len(fin) is 0:
        fin.append('false')
    return fin
        
def start_client():#main function for input and output
    inputfile = sys.argv[1]
    req=[]
    req=command_parser(inputfile)
    if ('false' in req):
        return
    src = int(inputfile[inputfile.find('h')+1:inputfile.find(".")])
    t1 =threading.Thread(name="Client Thread",target=client_agent(req,src)) 
    t1.start()
    #t1.join()    
    #print "Exit Main Thread"
    
start_client()
