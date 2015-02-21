1)How many VLANs do you have in your entire network? What is the minimum number of VLANs you need? Why?
Ans: In my entire network total number of VLAN is 240. I think we need minimum of 60 VLANs because if each edge switch knows the input and output port
and which host is connected to which port, we can effectively reduce 240 VLANs to 60 VLANs. Another way to think about it is that we have 4 unique paths
between every host destination pair. We have 240 unique host destination pair. So we need 240/4=60 VLANs.

2)Show the switch FIB table for a core, aggregator, and ToR switch. Then explain and describe how you planned to setup the FIB table, and how your routing
works.
Ans) FIB for ToR switch
 cookie=0x0, duration=1475.13s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=53 actions=output:3
 cookie=0x0, duration=1475.179s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=244 actions=output:4
 cookie=0x0, duration=1475.146s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=1,dl_vlan=57 actions=output:3
 cookie=0x0, duration=1475.176s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=1,dl_vlan=195 actions=output:4
 cookie=0x0, duration=1475.176s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=3,dl_vlan=146 actions=output:2
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=195 actions=output:4
 cookie=0x0, duration=1475.176s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=4,dl_vlan=258 actions=output:2
 cookie=0x0, duration=1475.146s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=1,dl_vlan=166 actions=output:3
 cookie=0x0, duration=1475.13s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=46 actions=output:3
 cookie=0x0, duration=1475.156s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=1,dl_vlan=251 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=104 actions=output:4
 cookie=0x0, duration=1475.153s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=1,dl_vlan=60 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=164 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=92 actions=output:4
 cookie=0x0, duration=1475.13s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=197 actions=output:3
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=220 actions=output:4
 cookie=0x0, duration=1475.13s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=45 actions=output:3
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=268 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=263 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=111 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=212 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=1,dl_vlan=48 actions=output:4
 cookie=0x0, duration=1475.147s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=71 actions=output:4
 cookie=0x0, duration=1475.13s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=166 actions=output:3
 cookie=0x0, duration=1475.176s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=4,dl_vlan=18 actions=output:2
 cookie=0x0, duration=1475.13s, table=0, n_packets=0, n_bytes=0, idle_age=1475, in_port=2,dl_vlan=270 actions=output:3



 FIB for Aggregator switch
  cookie=0x0, duration=1228.738s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=53 actions=output:1
 cookie=0x0, duration=1228.734s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=244 actions=output:3
 cookie=0x0, duration=1228.734s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=195 actions=output:3
 cookie=0x0, duration=1228.734s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=1,dl_vlan=195 actions=output:3
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=3,dl_vlan=183 actions=output:2
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=4,dl_vlan=103 actions=output:2
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=4,dl_vlan=71 actions=output:2
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=3,dl_vlan=104 actions=output:2
 cookie=0x0, duration=1228.713s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=1,dl_vlan=251 actions=output:4
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=4,dl_vlan=120 actions=output:2
 cookie=0x0, duration=1228.712s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=1,dl_vlan=60 actions=output:4
 cookie=0x0, duration=1228.734s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=164 actions=output:3
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,  in_port=2,dl_vlan=92 actions=output:4
 cookie=0x0, duration=1228.734s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=197 actions=output:1
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228, in_port=2,dl_vlan=220 actions=output:4
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=3,dl_vlan=39 actions=output:2
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228, in_port=2,dl_vlan=268 actions=output:4
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=111 actions=output:4
 cookie=0x0, duration=1228.734s, table=0, n_packets=0, n_bytes=0, idle_age=1228,in_port=2,dl_vlan=212 actions=output:3
 cookie=0x0, duration=1228.697s, table=0, n_packets=0, n_bytes=0, idle_age=1228, in_port=3,dl_vlan=263 actions=output:2
 cookie=0x0, duration=1228.71s, table=0, n_packets=0, n_bytes=0, idle_age=1228, in_port=1,dl_vlan=48 actions=output:4
 
 
 FIB for Core Switch
  cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=223 actions=output:4
 cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=48 actions=output:4
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=4,dl_vlan=171 actions=output:3
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=4,dl_vlan=139 actions=output:3
 cookie=0x0, duration=1428.777s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=112 actions=output:4
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=1,dl_vlan=251 actions=output:3
 cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=95 actions=output:4
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=1,dl_vlan=60 actions=output:3
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=4,dl_vlan=44 actions=output:3
 cookie=0x0, duration=1428.787s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=92 actions=output:3
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=4,dl_vlan=219 actions=output:3
 cookie=0x0, duration=1428.787s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=220 actions=output:3
 cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=79 actions=output:4
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=268 actions=output:3
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=1,dl_vlan=235 actions=output:3
 cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=144 actions=output:4
 cookie=0x0, duration=1428.777s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=271 actions=output:4
 cookie=0x0, duration=1428.777s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=111 actions=output:4
 cookie=0x0, duration=1428.784s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=1,dl_vlan=171 actions=output:3
 cookie=0x0, duration=1428.777s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=1,dl_vlan=48 actions=output:4
 cookie=0x0, duration=1428.777s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=1,dl_vlan=32 actions=output:4
 cookie=0x0, duration=1428.787s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=2,dl_vlan=156 actions=output:3
 cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=256 actions=output:4
 cookie=0x0, duration=1428.776s, table=0, n_packets=0, n_bytes=0, idle_age=1428, in_port=3,dl_vlan=63 actions=output:4

 How Routing works:
 
 To set-up connectivity I have used bottom up approach. Every edge/ToR router knows which hosts are connected to it on whcih port and so whenever it receives any flow
 destined to VLANs associated with a host it sends to the appropriate output port.
 To provide intra pod communication each edge switch either sends the flow to one of the host connected to that switch or sends it to left/right agrregator switch
 based on destination VLAN associated with hosts.
 To provide inter pod connectivity each pod sends the flow/packet to core switches based on whether destination host is connected to right/left side in a pod
 core switch 1 handles packet for host connected to left edge switch for pod 1 and 2.core switch 2 handles packet for host connected to left edge switch for pod 
 3 and 4.Same functionality by core switch 3 and 4 except now for the host connected to right edge switch.
 
 
 c) For a k=8 FatTree, how many hosts would we have? How many switches do we have? How many paths between a pair of hosts? How many VLANs do we need?
 Ans)  Host: 128
       Switches: 80 (16+32+32)
	   Total Paths = (k/2)^2 = 16
	   VLANs: 4064
	   
	   
Note: In my topology I have defined host to be connected to switch via port 1 and interface is h*-eth1
 

