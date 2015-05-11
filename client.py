#!/usr/bin/env python
import sys
import socket  
from collections import defaultdict
import socket
import time
import threading
import ctypes
import os




vlan=[[0],[0,0,331,491,651,811,971,1131,1291,1451,1611,1771,1931,2091,2251,2411,2571],[0,181,0,501,661,821,981,1141,1301,1461,1621,1781,1941,2101,2261,2421,2581],[0,191,351,0,671,831,991,1151,1311,1471,1631,1791,1951,2111,2271,2431,2591],[0,201,361,521,0,841,1001,1161,1321,1481,1641,1801,1961,2121,2281,1441,2601],[0,211,371,531,691,0,1011,1171,1331,1491,1651,1811,1971,2131,2291,2451,2611],[0,221,381,541,701,861,0,1181,1341,1501,1661,1821,1981,2141,2301,2461,2621],[0,231,391,551,711,871,1031,0,1351,1511,1671,1831,1991,2151,2311,2471,2631],[0,241,401,561,721,881,1041,1201,0,1521,1681,1841,2001,2161,2321,2481,2641],[0,251,411,571,731,891,1051,1211,1371,0,1691,1851,2011,2171,2331,2491,2651],[0,261,421,581,741,901,1061,1221,1381,1541,0,1861,2061,2181,2341,2501,2661],[0,271,431,591,751,911,1071,1231,1391,1551,1711,0,2031,2191,2351,2511,2671],[0,281,441,601,761,921,1081,1241,1401,1561,1721,1881,0,2201,2361,2521,2681],[0,291,451,611,771,931,1091,1251,1411,1571,1731,1891,2051,0,2371,2531,2691],[0,301,461,621,781,941,1101,1241,1421,1561,1741,1901,2061,2221,0,2541,2701],[0,311,471,631,791,951,1111,1251,1431,1591,1751,1911,2071,2231,2391,0,2711],[0,321,481,641,801,961,1121,1281,1441,1601,1761,1921,2081,2241,2401,2561]]
def send_packets(src, dest, port, ty, tpy):
    global vlan
    v=vlan[dest][src]
    #print v
    sleep = 80
    #if tpy == 'mix':
    #    sleep = 45
    #if tpy == 'perm':
    #    sleep = 45
    #print "Sleep", sleep, tpy
    pth = str(os.getcwd())+"/library.so"
    if (ty.find('K')) != -1:
        ctypes.CDLL(pth).sendPacket(v,int(ty.split('K')[0]),dest,src,port, sleep)
    if (ty.find('M')) != -1:
        #print "in m", (ty.split('M')[0])
        #for i in xrange (int(ty.split('M')[0])):
        ctypes.CDLL(pth).sendPacket(v,int(ty.split('M')[0]),dest,src,port, sleep)
        
def client_agent(req, src, tpy):
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
        ty=traffic_req[5]
        demand_str=demand_str+" "+str(dest)+" 4"
        #print demand_str
        try:
            def send_receive_demand(demand):
                host = socket.gethostname()
                alloc=''
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)         # Create a socket object# Get local machine name
                s.connect((arbiter_ip, prt))
                s.send(demand)
                alloc=s.recv(1024)
                return alloc
            allocation=send_receive_demand(demand_str)
        except Exception:
            pass
        send_packets(src, dest, port, ty, tpy)

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
    tpy = 'None'
    if (inputfile.find('perm')):
        tpy = 'perm'
    if (inputfile.find('mix')):
        tpy = 'mix'
    if (inputfile.find('incast')):
        tpy = 'incast'
    src = int(inputfile[inputfile.rfind('h')+1:inputfile.find(".")])
    t1 =threading.Thread(name="Client Thread",target=client_agent(req,src,tpy)) 
    t1.start()
    
start_client()
