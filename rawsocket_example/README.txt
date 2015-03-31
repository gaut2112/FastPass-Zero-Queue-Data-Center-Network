1. Here is the example that we used 
http://www.kanadas.com/program-e/2012/05/a_test_program_for_sendingrece.html
I have made a few changes for running in mininet example topology with two nodes (i.e., sudo mn)

2. To generate packet with specific VLAN (here I use VLAN=1, h1 MAC = d6363cc450a0, h2 MAC = 224ee8cd9100):
  
mininet@mininet-vm:~$ mininet/util/m h1 sudo ./sendrecv 0 1 0 1
eth0 terminal#=0 VLAN:1 srcMAC:0000d6363cc450a0 destMAC:0000224ee8cd9100
ifname = h1-eth0
Sent:     #0 (VLAN 1) from 0000d6363cc450a0 to 0000224ee8cd9100
Sent:     #1 (VLAN 1) from 0000d6363cc450a0 to 0000224ee8cd9100
Sent:     #2 (VLAN 1) from 0000d6363cc450a0 to 0000224ee8cd9100


3. To verify the packets are actually being sent, we use tcpdump at h1:

mininet@mininet-vm:~$ mininet/util/m h1 tcpdump -i h1-eth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on h1-eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
^C16:58:23.006161 d6:36:3c:c4:50:a0 (oui Unknown) > 22:4e:e8:cd:91:00 (oui Unknown), ethertype 802.1Q (0x8100), length 22:
        0x0000:  0000 0000                                ....
16:58:24.013931 d6:36:3c:c4:50:a0 (oui Unknown) > 22:4e:e8:cd:91:00 (oui Unknown), ethertype 802.1Q (0x8100), length 22:
        0x0000:  0000 0001                                ....
16:58:25.006970 d6:36:3c:c4:50:a0 (oui Unknown) > 22:4e:e8:cd:91:00 (oui Unknown), ethertype 802.1Q (0x8100), length 22:
        0x0000:  0000 0002                                ....

3 packets captured
3 packets received by filter
0 packets dropped by kernel

4. To verify the packets are actually being received, we use tcpdump at h2:

mininet@mininet-vm:~$ mininet/util/m h2 tcpdump -i h2-eth0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on h2-eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
^C17:07:50.011886 d6:36:3c:c4:50:a0 (oui Unknown) > 22:4e:e8:cd:91:00 (oui Unknown), ethertype 802.1Q (0x8100), length 22:
        0x0000:  0000 0000                                ....
17:07:51.008625 d6:36:3c:c4:50:a0 (oui Unknown) > 22:4e:e8:cd:91:00 (oui Unknown), ethertype 802.1Q (0x8100), length 22:
        0x0000:  0000 0001                                ....
17:07:52.005114 d6:36:3c:c4:50:a0 (oui Unknown) > 22:4e:e8:cd:91:00 (oui Unknown), ethertype 802.1Q (0x8100), length 22:
        0x0000:  0000 0002                                ....

3 packets captured
3 packets received by filter
0 packets dropped by kernel
3 packets dropped by interface

