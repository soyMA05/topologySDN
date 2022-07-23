from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, STATIC, StaticRoute

class MyTopology(IPTopo):
	def build(self, *args, **kwargs):
		# agregar routers solo con ipv4
		r1, r2, r3 = self.addRouters("r1", "r2", "r3", 
			config=RouterConfig, use_v4=True, use_v6=False)

		#crear switches
		s1,s2,s3 = [self.addSwitch(s) for s in ("s1","s2","s3")]

		#crear hosts
		h1,h2,h3,h4,h5,h6,h7,h8,h9 = [self.addHost(h) for h in ("h1","h2","h3","h4","h5","h6","h7","h8","h9")]

		#asignacion de IPs de enlace entre routers r1,r2,r3
		lr1r2 = self.addLink(r1, r2)
		lr1r2[r1].addParams(ip=("192.168.50.1/30"))
		lr1r2[r2].addParams(ip=("192.168.50.2/30"))
		
		lr2r3 = self.addLink(r2, r3)
		lr2r3[r2].addParams(ip=("192.168.50.5/30"))
		lr2r3[r3].addParams(ip=("192.168.50.6/30"))

		lr3r1 = self.addLink(r3, r1)
		lr3r1[r3].addParams(ip=("192.168.50.9/30"))
		lr3r1[r1].addParams(ip=("192.168.50.10/30"))

		#crear enlaces entre router y switch
		lr1s1 = self.addLink(r1, s1)
		lr1s1[r1].addParams(ip=("192.168.10.1/27"))

		lr2s2 = self.addLink(r2, s2)
		lr2s2[r2].addParams(ip=("192.168.20.1/25"))

		lr3s3 = self.addLink(r3, s3)
		lr3s3[r3].addParams(ip=("192.168.30.1/24"))

		#crear enlaces entre switch y hosts
		self.addLink(s1,h1,params2={"ip":"192.168.10.2/27"})
		self.addLink(s1,h2,params2={"ip":"192.168.10.3/27"})
		self.addLink(s1,h3,params2={"ip":"192.168.10.4/27"})
		self.addLink(s2,h4,params2={"ip":"192.168.20.2/25"})
		self.addLink(s2,h5,params2={"ip":"192.168.20.3/25"})
		self.addLink(s2,h6,params2={"ip":"192.168.20.4/25"})
		self.addLink(s3,h7,params2={"ip":"192.168.30.2/24"})
		self.addLink(s3,h8,params2={"ip":"192.168.30.3/24"})
		self.addLink(s3,h9,params2={"ip":"192.168.30.4/24"})

		# crear rutas predeterminadas
		r1.addDaemon(STATIC, static_routes=
				[StaticRoute("192.168.20.0/25","192.168.50.2"),
				StaticRoute("192.168.30.0/24","192.168.50.9")])
		r2.addDaemon(STATIC, static_routes=
				[StaticRoute("192.168.10.0/27","192.168.50.1"),
				StaticRoute("192.168.30.0/24","192.168.50.6")])
		r3.addDaemon(STATIC, static_routes=
				[StaticRoute("192.168.10.0/27","192.168.50.10"),
				StaticRoute("192.168.20.0/25","192.168.50.5")])

		super().build(*args, **kwargs)

#instanciar clase y red
net = IPNet(topo=MyTopology())
try:
	net.start()
	IPCLI(net)
finally:
	net.stop()
