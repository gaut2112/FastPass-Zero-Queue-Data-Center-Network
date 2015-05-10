from mininet.topo import Topo


class FatTopo(Topo):
    def __init__(self):
        
        Topo.__init__(self)
        for hosts in range(1,17):
            self.addHost("h"+str(hosts))
        for switch in range(1,21):
            self.addSwitch("s"+str(switch))
        self.createPod()
        self.createCoreAggLink()
        self.createEdgeHostLink()
        
    def createPod(self):
        #-------POD 1--------------#
        self.addLink("s1","s3",3,1)
        self.addLink("s1","s4",4,1)
        self.addLink("s2","s3",3,2)
        self.addLink("s2","s4",4,2)
        
        #----------POD 2--------------#
        self.addLink("s5","s7",3,1)
        self.addLink("s5","s8",4,1)
        self.addLink("s6","s7",3,2)
        self.addLink("s6","s8",4,2)
        #---------POD 3---------------#
        self.addLink("s9","s11",3,1)
        self.addLink("s9","s12",4,1)
        self.addLink("s10","s11",3,2)
        self.addLink("s10","s12",4,2)
        #----------POD 4--------------#
        self.addLink("s13","s15",3,1)
        self.addLink("s13","s16",4,1)
        self.addLink("s14","s15",3,2)
        self.addLink("s14","s16",4,2)
        
    def createCoreAggLink(self):
        #-------Core Switch 1 s17-----#
        self.addLink("s17","s3",1,3)
        self.addLink("s17","s7",2,3)
        self.addLink("s17","s11",3,3)
        self.addLink("s17","s15",4,3)
        #-------Core Switch 2 s18-----#
        self.addLink("s18","s3",1,4)
        self.addLink("s18","s7",2,4)
        self.addLink("s18","s11",3,4)
        self.addLink("s18","s15",4,4)
        #-------Core Switch 3 s19-----#
        self.addLink("s19","s4",1,3)
        self.addLink("s19","s8",2,3)
        self.addLink("s19","s12",3,3)
        self.addLink("s19","s16",4,3)
        #-------Core Switch 4 s20-----#
        self.addLink("s20","s4",1,4)
        self.addLink("s20","s8",2,4)
        self.addLink("s20","s12",3,4)
        self.addLink("s20","s16",4,4)
        
    def createEdgeHostLink(self):
        #Edge Switch 1- s1------------#
        self.addLink("s1","h1",1,0)
        self.addLink("s1","h2",2,0)
        #Edge Switch 2- s2------------#
        self.addLink("s2","h3",1,0)
        self.addLink("s2","h4",2,0)
        #Edge Switch 3-s5-------------#
        self.addLink("s5","h5",1,0)
        self.addLink("s5","h6",2,0)
        #Edge Switch 4 -s6------------#
        self.addLink("s6","h7",1,0)
        self.addLink("s6","h8",2,0)
        #Edge Switch 5 - s9-----------#
        self.addLink("s9","h9",1,0)
        self.addLink("s9","h10",2,0)
        #Edge Switch 6 - s10-----------#
        self.addLink("s10","h11",1,0)
        self.addLink("s10","h12",2,0)
        #Edge Switch 7 - s13-----------#
        self.addLink("s13","h13",1,0)
        self.addLink("s13","h14",2,0)
        #Edge Switch 8 - s14------------#
        self.addLink("s14","h15",1,0)
        self.addLink("s14","h16",2,0)
        
    @classmethod
    def create(cls):
        return cls()
        
topos = {"fattopo":FatTopo.create}
