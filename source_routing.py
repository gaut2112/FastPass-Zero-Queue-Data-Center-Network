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
        ofp        = dp.ofproto
        ofp_parser = dp.ofproto_parser

        # Make sure the switch's forwarding table is empty
        dp.send_delete_all_flows()
        
        # Creates a rule that sends out packets coming
        # from port: inport to the port: outport
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
            dest=[]
            vid = 0
            for i in range (1,17):
                if (i!= host):
                    vid = (i << 4)+ host
                    dest.append(vid)
                   # print dest
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
        # Rules for different switches
        if dp.id == 1:
            
            for vid in dest1:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 18)
            
            for vid in dest2:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 33)
            
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8+dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest5+dest6+dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 3, vid)
                    
        if dp.id == 2:
            
            for vid in dest3:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 52)
            
            for vid in dest4:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 67)
            
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6+dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 3, vid)
            for p in (1,2):
                for vid in dest7+dest8+dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 5:
            
            for vid in dest5:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 86)
            
            for vid in dest6:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 101)
            
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8+dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest1+dest2+dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 3, vid)
                    
        if dp.id == 6:
            
            for vid in dest7:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 120)
            
            for vid in dest8:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 135)
            
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6+dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 3, vid)
            for p in (1,2):
                for vid in dest3+dest4+dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 9:
            
            for vid in dest9:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 154)
            
            for vid in dest10:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 169)
            
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8+dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6+dest13+dest14:
                    from_port_to_port(p, 3, vid)
                    
        if dp.id == 10:
            
            for vid in dest11:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 188)
            
            for vid in dest12:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 203)
            
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6+dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 3, vid)
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8+dest15+dest16:
                    from_port_to_port(p, 4, vid)
                    

                    
        if dp.id == 13:
            
            for vid in dest13:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 222)
            
            for vid in dest14:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 237)
            
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6+dest9+dest10:
                    from_port_to_port(p, 3, vid)
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8+dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 14:
            
            for vid in dest15:
                from_port_to_port(3, 1, vid)
                from_port_to_port(4, 1, vid)
            from_port_to_port(1, 2, 256)
            
            for vid in dest16:
                from_port_to_port(3, 2, vid)
                from_port_to_port(4, 2, vid)
            from_port_to_port(2, 1, 271)
            
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8+dest11+dest12:
                    from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6+dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 3, vid)
                    
        if dp.id == 3:
            
            for p in (2,3,4):
                for vid in dest1+dest2:
                    from_port_to_port(p, 1, vid)
            for p in (1,2):
		for vid in dest5+dest6:
		    from_port_to_port(p,3,vid)
            for p in (1,2):
                for vid in dest9+dest10+dest13+dest14:
                    from_port_to_port(p, 4, vid)
            
            for vid in dest3+dest4:
                from_port_to_port(1, 2, vid)
                    
        if dp.id == 4:
            
            for p in (1,3,4):
                for vid in dest3+dest4:
                    from_port_to_port(p, 2, vid)
            for p in (1,2):
		for vid in dest7+dest8:
		    from_port_to_port(p,3,vid)
            for p in (1,2):
                for vid in dest11+dest12+dest15+dest16:
                    from_port_to_port(p, 4, vid)
            for vid in dest1+dest2:
                from_port_to_port(2, 1, vid)
                    
        if dp.id == 7:
            for vid in dest7+dest8:
                from_port_to_port(1, 2, vid)
            
            for p in (2,3,4):
                for vid in dest5+dest6:
                    from_port_to_port(p, 1, vid)
            for p in (1,2):
		for vid in dest9+dest10+dest13+dest14:
		    from_port_to_port(p, 4, vid)
            for p in (1,2):
                for vid in dest1+dest2:
                    from_port_to_port(p, 3, vid)
                    
        if dp.id == 8:
            for vid in dest5+dest6:
                from_port_to_port(2, 1, vid)
            
            for p in (1,2):
		for vid in dest3+dest4:
		    from_port_to_port(p, 3, vid)
	    for p in (1,2):
		for vid in dest11+dest12+dest15+dest16:
		    from_port_to_port(p, 4, vid)
	    for p in (1,3,4):
                for vid in dest7+dest8:
                    from_port_to_port(p, 2, vid)
                    
        if dp.id == 11:
            
            for p in (2,3,4):
                for vid in dest9+dest10:
                    from_port_to_port(p, 1, vid)
            
            for p in (1,2):
                for vid in dest5+dest6+dest1+dest2:
                    from_port_to_port(p, 3, vid)
            
            for p in (1,2):
                for vid in dest13+dest14:
                    from_port_to_port(p, 4, vid)
            
                    
            for vid in dest11+dest12:
                from_port_to_port(1, 2, vid)
                    
        if dp.id == 12:
            
            for p in (1,3,4):
                for vid in dest11+dest12:
                    from_port_to_port(p, 2, vid)
            
            for p in (1,2):
                for vid in dest7+dest8+dest3+dest4:
                    from_port_to_port(p, 3, vid)
                    
            for vid in dest9+dest10:
                from_port_to_port(2, 1, vid)
                    
            for p in (1,2):
                for vid in  dest15+dest16:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 15:
            for vid in dest15+dest16:
                from_port_to_port(1, 2, vid)
            
            for p in (2,3,4):
                for vid in dest13+dest14:
                    from_port_to_port(p, 1, vid)
            
            for p in (1,2):
                for vid in dest1+dest2+dest5+dest6:
                    from_port_to_port(p, 3, vid)
            for p in (1,2):
                for vid in dest9+dest10:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 16:
            for vid in dest13+dest14:
                from_port_to_port(2, 1, vid)
            
            for p in (1,3,4):
                for vid in dest15+dest16:
                    from_port_to_port(p, 2, vid)
            
            for p in (1,2):
                for vid in dest3+dest4+dest7+dest8:
                    from_port_to_port(p, 3, vid)
            for p in (1,2):
                for vid in dest11+dest12:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 17:
            
            for p in (2,3,4):
                for vid in dest1+dest2:
                    from_port_to_port(p, 1, vid)
	    for p in (1,2,4):
		for vid in dest9+dest10:
		    from_port_to_port(p,3,vid)
	    for p in (1,2,3):
		for vid in dest13+dest14:
		    from_port_to_port(p,4,vid)
            for p in (1,3,4):
                for vid in dest5+dest6:
                    from_port_to_port(p, 2, vid)
                    
        if dp.id == 18:
            
            for p in (2,1,4):
                for vid in dest9+dest10:
                    from_port_to_port(p, 3, vid)
            for p in (1,3,2):
                for vid in dest13+dest14:
                    from_port_to_port(p, 4, vid)
                    
        if dp.id == 19:
            #for p in (1,2,4):
		#for vid in dest11+dest12:
		    #from_port_to_port(p,3,vid)
            for p in (2,3,4):
                for vid in dest3+dest4:
                    from_port_to_port(p, 1, vid)
            for p in (1,3,4):
                for vid in dest7+dest8:
                    from_port_to_port(p, 2, vid)
                    
        if dp.id == 20:
            
            for p in (2,4,1):
                for vid in dest11+dest12:
                    from_port_to_port(p, 3, vid)
            for p in (1,2,3):
                for vid in dest15+dest16:
                    from_port_to_port(p, 4, vid)
                    
        
                    
        
            
                    
                
            
 



