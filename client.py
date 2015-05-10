#!/usr/bin/env python
import sys
import socket  
from collections import defaultdict
import socket
import time
import threading
import ctypes
import os




vlan=[[0],[0,0,331,492,652,811,972,1131,1292,1451,1612,1771,1932,2091,2252,2411,2572],[0,181,0,502,661,822,981,1142,1301,1462,1621,1782,1941,2102,2261,2422,2581],[0,191,352,0,671,832,991,1152,1311,1472,1631,1792,1951,2112,2271,2432,2591],[0,201,362,521,0,842,1001,1162,1321,1482,1641,1802,1961,2122,2281,1442,2601],[0,211,372,531,692,0,1011,1172,1331,1492,1651,1812,1971,2132,2291,2452,2611],[0,221,382,543,702,861,0,1182,1341,1502,1661,1822,1981,2142,2301,2462,2621],[0,231,392,551,712,871,1031,0,1351,1512,1671,1832,1991,2152,2311,2472,2631],[0,241,402,561,722,881,1042,1201,0,1522,1681,1842,2001,2162,2321,2482,2641],[0,251,412,571,732,891,1052,1211,1372,0,1691,1852,2011,2172,2331,2492,2651],[0,261,422,581,742,901,1062,1221,1381,1541,0,1862,2061,2182,2341,2502,2661],[0,271,433,591,752,911,1072,1231,1391,1551,1712,0,2031,2192,2351,2512,2671],[0,281,442,601,762,921,1082,1241,1401,1561,1722,1881,0,2202,2361,2522,2681],[0,291,452,611,772,931,1092,1251,1411,1571,1732,1891,2052,0,2371,2532,2691],[0,301,462,621,782,941,1102,1241,1421,1561,1742,1901,2062,2221,0,2542,2701],[0,311,472,631,792,951,1112,1251,1431,1591,1752,1911,2072,2231,2391,0,2711],[0,321,482,641,802,961,1122,1281,1442,1601,1762,1921,2082,2241,2402,2561]]
def send_packets(src, dest, port, ty):
    global vlan
    v=vlan[dest][src]
    print v
    pth = str(os.getcwd())+"/library.so"
    if (ty.find('K')) != -1:
        ctypes.CDLL(pth).sendPacket(v,int(ty.split('K')[0])*120,dest,src,port)
    if (ty.find('M')) != -1:
        #print "in m", (ty.split('M')[0])
        #for i in xrange (int(ty.split('M')[0])):
        ctypes.CDLL(pth).sendPacket(v,int(ty.split('M')[0])*1200,dest,src,port)
        
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
            #allocation=send_receive_demand(demand_str)
        except Exception:
            pass
        send_packets(src, dest, port, ty)

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
    
start_client()
