from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.util import pmonitor
from mininet.log import setLogLevel, info
from mininet.cli import CLI

import os
from time import sleep

# Create Topology

class Topology(Topo):
	def create_cluster(self, clients, bw, name):
		S = self.addSwitch(name)
		for c in clients:
			self.addLink(S, c, bw=min(1000, bw))
		return S

	def return_servers(self):
		return self.servers

	def return_clients(self):
		return self.clients

	def build(self, bw, num_servers, cluster_size, num_client_clusters):
		# Complete client list
		self.clients = {}
		# Add main gateway switch
		main_gateway = self.addSwitch('switchm0')
		# Add main switch
		main_switch = self.addSwitch('switchm1')

		self.addLink(main_gateway, main_switch, bw=1000)
		# Add DB server
		db_server = self.addHost('db_server')
		# Add servers
		self.servers = [self.addHost('server_{}'.format(j)) for j in range(num_servers)]
		# Link gateway with db server
		self.addLink(main_gateway, db_server, bw=1000)
		# Link servers with gateway
		for s in self.servers:
			self.addLink(main_gateway, s, bw=1000)

		# Creating clusters
		switches = []
		for i in range(num_client_clusters):
			clients = {'client_{}_{}'.format(i, j):self.addHost('client{}s{}'.format(i, j)) for j in range(cluster_size)}
			self.clients.update(clients)
			switches.append(self.create_cluster(clients.values(), bw, 'switch{}'.format(i)))

		ll = num_client_clusters//5

		bswitches = []

		for i in range(ll):
			clients = switches[i*5:i*5+5]
			bswitches.append(self.create_cluster(clients, bw*cluster_size, 'switchb{}'.format(i)))

		for b in bswitches:
			self.addLink(main_switch, b, bw=min(bw*cluster_size*5, 1000))
		for s in switches[ll*5:]:
			self.addLink(main_switch, s, bw=min(bw*cluster_size, 1000))


def main():
	bw = 7
	num_servers = 4
	cluster_size = 5
	num_client_clusters = 20

	net = Mininet(Topology(
		bw=bw, num_servers=num_servers, cluster_size=cluster_size, num_client_clusters=num_client_clusters
		), link=TCLink,cleanup=True)

	net.start()

	db_server = net.get('db_server')

	with open('config', 'w') as fp:
		fp.write('export HOST={}\n'.format(db_server.IP()))
		fp.write('export DB=twitter\n')
		fp.write('export USER=postgres\n')
		fp.write('export PASS=postgres\n')

	os.environ['HOST'] = db_server.IP()
	os.environ['DB'] = 'twitter'
	os.environ['USER'] = 'postgres'
	os.environ['PASS'] = 'postgres'

	popens = {}

	db_server.popen("sudo -u postgres /usr/lib/postgresql/10/bin/postgres -p 5432 -D /etc/postgresql/10/main2")

	sleep(10)

	CLI(net)

	servers = net.topo.return_servers()
	clients = net.topo.return_clients()
	keys = list(clients.keys())

	for s in servers:
		net.get(s).popen("python3 main.py")

	for i in range(num_client_clusters):
		for j in range(cluster_size):
			ind = i*cluster_size+j
			popens[keys[ind]] = net.get(clients[keys[ind]]).popen(
				"python3 client.py {} {} {} {} {}:8080".format(j, i, num_client_clusters, cluster_size, net.get(servers[ind%num_servers]).IP())
				)
	for host, line in pmonitor( popens ):
		if host:
			info( "<%s>: %s" % ( host, line ) )
	for s in servers:
		net.get(s).terminate()
	db_server.terminate()

	net.stop()


if __name__=='__main__':
	setLogLevel( 'info' )
	main()