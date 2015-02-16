from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import *
from mininet.nodelib import LinuxBridge

from optparse import OptionParser
import os, sys

ARBITER_IP="20.0.0.100/32"

# Connects all the host in the network to the root
# Namespace.  This enables the nodes to communicate with
# Arbiter, by using the 20.0.0.100 IP address.
def connect_hosts_to_root_ns(net):
	sw   = LinuxBridge('rtsw', dpid="001020203")
	root = Node('root', inNamespace=False)
	root0 = net.addLink(root, sw)

	for host in net.hosts:
		ip = ""

		# Get the IP of the other interface
		try:
			ip = host.intfList()[0].ip
			ip = "20." + ".".join(ip.split(".")[1:])
		except Exception:
			print ("Failed to get the IP address of your interface."
				+ "  The offending host is: " + str(host))
			return False

		link = net.addLink(sw, host)
		host.cmd('ifconfig ' + str(link.intf2) + ' ' + str(ip) + '/24')
		
	root.setIP(ARBITER_IP, intf=root0.intf1)
	root.cmd('route add -net 20.0.0.0/24 dev ' + str(root0.intf1));
	sw.start([])
	return True


def parse_options():
	parser = OptionParser()
	parser.add_option("-c", "--custom", dest="custom",
	    	help="The custom topology file.")
	parser.add_option("-t", "--topo", dest="topo", 
	    	help="Name of the topology in the topos dictionary")
	return parser.parse_args()

def module_name_from_file(filename):
	return os.path.splitext(filename)[0]

if __name__ == '__main__':
	(options, args) = parse_options()

	print ("Importing the topology file.")
	topo = __import__(module_name_from_file(options.custom))

	print ("Initiating Mininet.")
	net = Mininet(topo.topos[options.topo](), controller=RemoteController)

	print ("Initiating the Arbiter network.")
	if (not connect_hosts_to_root_ns(net)):
		print("Failed to create the Arbiter network.")
		sys.exit()


	print ("Hosts can access the Arbiter at: " + str(ARBITER_IP))
	net.start()

	print ("Initiating Mininet CLI.")
	CLI(net)

	net.stop()
