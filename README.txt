1. Did you use code from anywhere for your project? If not, say so. If so, say what functions and where they are from. (Also mark these codes with a comment in
the source code.)

Ans: 
--> raw_sockets.c : The raw socket code has been taken from 
    1)https://austinmarton.wordpress.com/2011/09/14/sending-raw-ethernet-packets-from-a-specific-interface-in-c-on-linux/
    2)https://gist.github.com/austinmarton/1922600
    
--> client.py : The integration of python and C is taken from this example from stack overflow:
    http://stackoverflow.com/questions/4241415/import-c-function-into-python-program
    
    
2. List all the detailed changes you have made from Project B to Project C. And why each change helps the performance.

Ans: 

--> In project B I have used only 2 VLANs in project C I am randomly allocating from 4 VLANs to randomize overall traffic. For
    generating VLAN's, I have used strawmans approach with adding (1,2,3,4). 
--> Instead of retransmission, I have opted to send around 1.1 time the traffic to simplfly the architecture.
--> I have opted against batch request to reuse project B architecture.
--> I am pacing the packets by sleeping for 150ms for each batch of 200 packets. This helps in managing qqueue in switches.




