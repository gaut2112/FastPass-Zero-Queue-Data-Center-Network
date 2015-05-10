from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
import itertools


class Controller(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)


    @set_ev_cls(dpset.EventDP, MAIN_DISPATCHER)
    def switch_in(self, ev):
        dp  = ev.dp
        entered = ev.enter
        if ev.enter:
            self.install_rules(dp)


    def install_rules(self, dp):
        
        hostpair=[[1,2],[3,4],[5,6],[7,8],[9,10],[11,12],[13,14],[15,16]]
        samepod=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        ofp        = dp.ofproto
        ofp_parser = dp.ofproto_parser

        # Make sure the switch's forwarding table is empty
        dp.send_delete_all_flows()
        
        # Creates a rule that sends out packets coming
        # from port: inport to the port: outport
        def same_pod(host,i,lst):
            for pod in lst:
                if host in pod:
                    if i in pod:
                        return True
            return False
        
        
        def from_port_to_port(inport, outport, vlanid):
            match   = ofp_parser.OFPMatch(in_port=inport,dl_vlan=vlanid)
            actions = [ofp_parser.OFPActionOutput(outport)]
            out     = ofp_parser.OFPFlowMod(
                    datapath=dp, cookie=0,
                    command=ofp.OFPFC_ADD,
                    match=match,
                    actions=actions)
            dp.send_msg(out)
        def createVlanId(host):
            dest=[[],[],[]]
            vid = 0
            for i in range (1,17):
                if (i!= host):
                    vid = (i << 4)+ host
                    if ([host,i] in hostpair or [i,host] in hostpair):
                        dest[0].append(vid*10+1)
                    elif (same_pod(host,i,samepod)):
                        dest[1].append(vid*10+1)
                        dest[1].append(vid*10+2)
                    else:
                        dest[2].append(vid*10+1)
                        dest[2].append(vid*10+2)
                        dest[2].append(vid*10+3)
                        dest[2].append(vid*10+4)
            return dest
        dest1=createVlanId(1)
        dest2=createVlanId(2)
        dest3=createVlanId(3)
        dest4=createVlanId(4)
        dest5=createVlanId(5)
        dest6=createVlanId(6)
        dest7=createVlanId(7)
        dest8=createVlanId(8)
        dest9=createVlanId(9)
        dest10=createVlanId(10)
        dest11=createVlanId(11)
        dest12=createVlanId(12)
        dest13=createVlanId(13)
        dest14=createVlanId(14)
        dest15=createVlanId(15)
        dest16=createVlanId(16)
        #print "dest 1"+str(dest1)
        #print "dest 2"+str(dest2)
            
        # Rules for different switches
        #start POD1
        if dp.id == 1:
            
            for vid in dest1[1]+dest1[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 181)
            
            for vid in dest2[1]+dest2[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 331)
            #same pod
            for p in (1,2):
                for vid in dest3[1]+dest4[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 3 and 4
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            
            #different pod
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 3 and 4
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 3, vid)
                        
                    
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 3 and 4
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 3, vid)
                    
        if dp.id == 2:
            
            for vid in dest3[1]+dest3[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 521)
            
            for vid in dest4[1]+dest4[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 671)
            #same pod
            for p in (1,2):
                for vid in dest1[1]+dest2[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 3 and 4
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            #different pod
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 4, vid)
                    
        if dp.id == 3:
            for vid in dest3[1]+dest4[1]:
                from_port_to_port(1,2,vid)
                
            for vid in dest1[1]+dest2[1]:
                from_port_to_port(2,1,vid)
                
            for p in (3,4):
                for vid in dest1[2]+dest2[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 1, vid)
            for p in (3,4):
                for vid in dest3[2]+dest4[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 2, vid)
                    
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==2:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==3:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==4:
                        from_port_to_port(p, 4, vid)
                    
        if dp.id == 4:
            for vid in dest1[1]+dest2[1]:
                from_port_to_port(2,1,vid)
                
            for vid in dest3[1]+dest4[1]:
                from_port_to_port(1,2,vid)
                
            for p in (3,4):
                for vid in dest3[2]+dest4[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 2, vid)
            for p in (3,4):
                for vid in dest1[2]+dest2[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 1, vid)
                        
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==3:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==4:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==1:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==2:
                        from_port_to_port(p, 4, vid)
                    
                #end POD 1
                
                #start POD 2
        if dp.id == 5:
            for vid in dest5[1]+dest5[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 861)
            
            for vid in dest6[1]+dest6[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 1011)
            #same POD
            for p in (1,2):
                for vid in dest7[1]+dest8[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 7 and 8
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same POD
            #Different POD
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 7 and 8
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 4, vid)
                        
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 3, vid)
            
                    
        if dp.id == 6:
            #same Tor
            for vid in dest7[1]+dest7[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 1201)
            
            for vid in dest8[1]+dest8[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 1351)
            #end same tor
            #same pod
            for p in (1,2):
                for vid in dest5[1]+dest6[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 7 and 8
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            #different POD
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 4, vid)
            #end different POD      
        if dp.id == 7:
            for vid in dest7[1]+dest8[1]:
                from_port_to_port(1,2,vid)
                
            for vid in dest5[1]+dest6[1]:
                from_port_to_port(2,1,vid)
                
            for p in (3,4):
                for vid in dest5[2]+dest6[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 1, vid)
            for p in (3,4):
                for vid in dest7[2]+dest8[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 2, vid)
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==2:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==3:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==4:
                        from_port_to_port(p, 4, vid)
                    
        if dp.id == 8:
            for vid in dest5[1]+dest6[1]:
                from_port_to_port(2,1,vid)
                
            for vid in dest7[1]+dest8[1]:
                from_port_to_port(1,2,vid)
                
            for p in (3,4):
                for vid in dest7[2]+dest8[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 2, vid)
            for p in (3,4):
                for vid in dest5[2]+dest6[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 1, vid)
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest9[2]+dest10[2]+dest13[2]+dest14[2]:
                    if vid%10 ==3:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==4:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest11[2]+dest12[2]+dest15[2]+dest16[2]:
                    if vid%10 ==1:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==2:
                        from_port_to_port(p, 4, vid)
              
        if dp.id == 9:
            
            for vid in dest9[1]+dest9[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 1541)
            
            for vid in dest10[1]+dest10[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 1691)
            #same pod
            for p in (1,2):
                for vid in dest11[1]+dest12[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 11 and 12
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            
            #different pod
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest3[2]+dest4[2]+dest15[2]+dest16[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 11 and 12
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 3, vid)
                        
                    
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest1[2]+dest2[2]+dest13[2]+dest14[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 11 and 12
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 3, vid)
                    
        if dp.id == 10:
            
            for vid in dest11[1]+dest11[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 1881)
            
            for vid in dest12[1]+dest12[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 2031)
            #same pod
            for p in (1,2):
                for vid in dest9[1]+dest10[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 3 and 4
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            #different pod
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest1[2]+dest2[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest3[2]+dest4[2]+dest15[2]+dest16[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 4, vid)
            #end different POD
        if dp.id == 11:
            
            for vid in dest11[1]+dest12[1]:
                from_port_to_port(1,2,vid)
                
            for vid in dest9[1]+dest10[1]:
                from_port_to_port(2,1,vid)
                
            for p in (3,4):
                for vid in dest9[2]+dest10[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 1, vid)
            for p in (3,4):
                for vid in dest11[2]+dest12[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 2, vid)
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest5[2]+dest6[2]+dest13[2]+dest14[2]:
                    if vid%10 ==1:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==2:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest7[2]+dest8[2]+dest15[2]+dest16[2]:
                    if vid%10 ==3:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==4:
                        from_port_to_port(p, 4, vid)
                    
        if dp.id == 12:
            
            for vid in dest9[1]+dest10[1]:
                from_port_to_port(2,1,vid)
                
            for vid in dest11[1]+dest12[1]:
                from_port_to_port(1,2,vid)
                
            for p in (3,4):
                for vid in dest11[2]+dest12[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 2, vid)
            for p in (3,4):
                for vid in dest9[2]+dest10[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 1, vid)
                        
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest5[2]+dest6[2]+dest13[2]+dest14[2]:
                    if vid%10 ==3:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==4:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest7[2]+dest8[2]+dest15[2]+dest16[2]:
                    if vid%10 ==1:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==2:
                        from_port_to_port(p, 4, vid)
            #END POD 3
            
            #START POD 4
        if dp.id == 13:
            
            for vid in dest13[1]+dest13[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 2221)
            
            for vid in dest14[1]+dest14[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 2371)
            #same pod
            for p in (1,2):
                for vid in dest15[1]+dest16[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 15 and 16
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            
            #different pod
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest3[2]+dest4[2]+dest11[2]+dest12[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 15 and 16
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 3, vid)
                        
                    
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest1[2]+dest2[2]+dest9[2]+dest10[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 15 and 16
                        from_port_to_port(p, 4, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 3, vid)
                    
        if dp.id == 14:
            
            for vid in dest15[1]+dest15[2]:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 2561)
            
            for vid in dest16[1]+dest16[2]:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1,2711)
            #same pod
            for p in (1,2):
                for vid in dest13[1]+dest14[1]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)#make changes in switch 3 and 4
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            #end same pod
            #different pod
            for p in (1,2):
                for vid in dest5[2]+dest6[2]+dest1[2]+dest2[2]+dest9[2]+dest10[2]:
                    if vid%10 ==1 or vid%10 ==2:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==3 or vid%10 ==4:
                        from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest7[2]+dest8[2]+dest3[2]+dest4[2]+dest11[2]+dest12[2]:
                    if vid%10 ==3 or vid%10 ==4:    #make changes in switch 3 and 4
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==1 or vid%10 ==2:
                        from_port_to_port(p, 4, vid)
            #end different POD
                    
                    
        if dp.id == 15:
            for vid in dest15[1]+dest16[1]:
                from_port_to_port(1,2,vid)
                
            for vid in dest13[1]+dest14[1]:
                from_port_to_port(2,1,vid)
                
            for p in (3,4):
                for vid in dest13[2]+dest14[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 1, vid)
            for p in (3,4):
                for vid in dest15[2]+dest16[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 2, vid)
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest5[2]+dest6[2]+dest9[2]+dest10[2]:
                    if vid%10 ==1:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==2:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest7[2]+dest8[2]+dest11[2]+dest12[2]:
                    if vid%10 ==3:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==4:
                        from_port_to_port(p, 4, vid)
                    
        if dp.id == 16:
            for vid in dest13[1]+dest14[1]:
                from_port_to_port(2,1,vid)
                
            for vid in dest15[1]+dest16[1]:
                from_port_to_port(1,2,vid)
                
            for p in (3,4):
                for vid in dest15[2]+dest16[2]:
                    if vid%10==1 or vid%10==2:
                        from_port_to_port(p, 2, vid)
            for p in (3,4):
                for vid in dest13[2]+dest14[2]:
                    if vid%10==3 or vid%10==4:
                        from_port_to_port(p, 1, vid)
                        
            for p in (1,2):
                for vid in dest1[2]+dest2[2]+dest5[2]+dest6[2]+dest9[2]+dest10[2]:
                    if vid%10 ==3:
                        from_port_to_port(p,3,vid)
                    if vid%10 ==4:
                        from_port_to_port(p,4,vid)
            for p in (1,2):
                for vid in dest3[2]+dest4[2]+dest7[2]+dest8[2]+dest11[2]+dest12[2]:
                    if vid%10 ==1:
                        from_port_to_port(p, 3, vid)
                    if vid%10 ==2:
                        from_port_to_port(p, 4, vid)
        #start CORE switches
                   
        if dp.id == 17:
            
            for p in (2,3,4):
                for vid in dest1[2]+dest2[2]:
                    if vid % 10==1:
                        from_port_to_port(p, 1, vid)
            for p in (2,3,4):
                for vid in dest3[2]+dest4[2]:
                    if vid % 10==3:
                        from_port_to_port(p, 1, vid)
                        
                        
            for p in (1,3,4):
                for vid in dest5[2]+dest6[2]:
                    if vid%10 ==1:
                        from_port_to_port(p, 2, vid)
            for p in (1,3,4):
                for vid in dest7[2]+dest8[2]:
                    if vid%10 ==3:
                        from_port_to_port(p, 2, vid)
                        
                        
            for p in (1,2,4):
                for vid in dest9[2]+dest10[2]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)
            for p in (1,2,4):
                for vid in dest11[2]+dest12[2]:
                    if vid%10==3:
                        from_port_to_port(p, 3, vid)
                        
                        
            for p in (1,2,3):
                for vid in dest13[2]+dest14[2]:
                    if vid%10==1:
                        from_port_to_port(p, 4, vid)
            for p in (1,2,3):
                for vid in dest15[2]+dest16[2]:
                    if vid%10==3:
                        from_port_to_port(p, 4, vid)
        if dp.id == 18:
            
            for p in (2,3,4):
                for vid in dest1[2]+dest2[2]:
                    if vid % 10==2:
                        from_port_to_port(p, 1, vid)
            for p in (2,3,4):
                for vid in dest3[2]+dest4[2]:
                    if vid % 10==4:
                        from_port_to_port(p, 1, vid)
                        
                        
            for p in (1,3,4):
                for vid in dest5[2]+dest6[2]:
                    if vid%10 ==2:
                        from_port_to_port(p, 2, vid)
            for p in (1,3,4):
                for vid in dest7[2]+dest8[2]:
                    if vid%10 ==4:
                        from_port_to_port(p, 2, vid)
                        
                        
            for p in (1,2,4):
                for vid in dest9[2]+dest10[2]:
                    if vid%10==2:
                        from_port_to_port(p, 3, vid)
            for p in (1,2,4):
                for vid in dest11[2]+dest12[2]:
                    if vid%10==4:
                        from_port_to_port(p, 3, vid)
                        
                        
            for p in (1,2,3):
                for vid in dest13[2]+dest14[2]:
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
            for p in (1,2,3):
                for vid in dest15[2]+dest16[2]:
                    if vid%10==4:
                        from_port_to_port(p, 4, vid)
                    
        if dp.id == 19:
            for p in (2,3,4):
                for vid in dest1[2]+dest2[2]:
                    if vid % 10==3:
                        from_port_to_port(p, 1, vid)
            for p in (2,3,4):
                for vid in dest3[2]+dest4[2]:
                    if vid % 10==1:
                        from_port_to_port(p, 1, vid)
                        
                        
            for p in (1,3,4):
                for vid in dest5[2]+dest6[2]:
                    if vid%10 ==3:
                        from_port_to_port(p, 2, vid)
            for p in (1,3,4):
                for vid in dest7[2]+dest8[2]:
                    if vid%10 ==1:
                        from_port_to_port(p, 2, vid)
                        
            for p in (1,2,4):
                for vid in dest9[2]+dest10[2]:
                    if vid%10==3:
                        from_port_to_port(p, 3, vid)
            for p in (1,2,4):
                for vid in dest11[2]+dest12[2]:
                    if vid%10==1:
                        from_port_to_port(p, 3, vid)
                        
                        
            for p in (1,2,3):
                for vid in dest13[2]+dest14[2]:
                    if vid%10==3:
                        from_port_to_port(p, 4, vid)
            for p in (1,2,3):
                for vid in dest15[2]+dest16[2]:
                    if vid%10==1:
                        from_port_to_port(p, 4, vid)
            

                    
        if dp.id == 20:
            for p in (2,3,4):
                for vid in dest1[2]+dest2[2]:
                    if vid % 10==4:
                        from_port_to_port(p, 1, vid)
            for p in (2,3,4):
                for vid in dest3[2]+dest4[2]:
                    if vid % 10==2:
                        from_port_to_port(p, 1, vid)
                        
                        
            for p in (1,3,4):
                for vid in dest5[2]+dest6[2]:
                    if vid%10 ==4:
                        from_port_to_port(p, 2, vid)
            for p in (1,3,4):
                for vid in dest7[2]+dest8[2]:
                    if vid%10 ==2:
                        from_port_to_port(p, 2, vid)
                        
                        
            for p in (1,2,4):
                for vid in dest9[2]+dest10[2]:
                    if vid%10==4:
                        from_port_to_port(p, 3, vid)
            for p in (1,2,4):
                for vid in dest11[2]+dest12[2]:
                    if vid%10==2:
                        from_port_to_port(p, 3, vid)
                        
            for p in (1,2,3):
                for vid in dest13[2]+dest14[2]:
                    if vid%10==4:
                        from_port_to_port(p, 4, vid)
            for p in (1,2,3):
                for vid in dest15[2]+dest16[2]:
                    if vid%10==2:
                        from_port_to_port(p, 4, vid)
                    
        
                    
        
            
                    
                
            
 



