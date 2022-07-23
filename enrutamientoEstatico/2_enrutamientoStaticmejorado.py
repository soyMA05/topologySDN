"""agregar propiedades de configuracion con redes IP"""
from ipmininet.ipnet import IPNet
"""uso de cli de mininet"""
from ipmininet.cli import IPCLI
"""creacion de topologias personalizadas"""
from ipmininet.iptopo import IPTopo
"""configuracion de protocolos de enrutamiento"""
from ipmininet.router.config import RouterConfig, STATIC, StaticRoute

"""crear clase para crear topologias"""
class MyTopology(IPTopo):
	"""metodo modo constructor"""
	def build(self, *args, **kwargs):

		""" agregar routers solo con ipv4"""
		r1, r2, r3 = self.addRouters("r1", "r2", "r3", config=RouterConfig, use_v4=True, use_v6=False)

		"""crear switches"""
		s1,s2,s3 = [self.addSwitch(s) for s in ("s1","s2","s3")]

		"""crear hosts"""
		h1,h2,h3,h4,h5,h6,h7,h8,h9 = [self.addHost(h) for h in ("h1","h2","h3","h4","h5","h6","h7","h8","h9")]

		"""crear listas con los dispositivos de red"""
		ro=[r1,r2,r3]
		sw=[s1,s2,s3]
		hosts=[h1,h2,h3,h4,h5,h6,h7,h8,h9]

		"""asignacion de IPs de enlace entre routers r1,r2,r3"""
		ips_enlace=["192.168.50.1/30","192.168.50.2/30","192.168.50.5/30","192.168.50.6/30","192.168.50.9/30","192.168.50.10/30"]
		j=0
		for rs,rd in zip(ro,[r2,r3,r1]):
			self.addLink(rs,rd,params1={"ip":ips_enlace[j]},params2={"ip":ips_enlace[j+1]})
			j+=2

		"""crear enlaces entre router y switch, mas asignacion de ip red LAN"""
		ip_redLan=["192.168.10.1/27","192.168.20.1/25","192.168.30.1/24"]
		for i in range(0,3):
			self.addLink(ro[i], sw[i], params1={"ip":ip_redLan[i]})

		"""crear enlaces entre switch y hosts, mas asignacion de ip en hosts"""
		ip_host=["192.168.10.2/27","192.168.10.3/27","192.168.10.4/27","192.168.20.2/25","192.168.20.3/25",
			"192.168.20.4/25","192.168.30.2/24","192.168.30.3/24","192.168.30.4/24"]
		j=1
		k=0
		for h,iph in zip(hosts,ip_host):
			self.addLink(sw[k],h,params2={"ip":iph})
			if j%3==0:
				k+=1
			j+=1

		"""crear rutas predeterminadas"""
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

"""instanciar clase de red con parametro de topologia personalizada"""
net = IPNet(topo=MyTopology())
try:
	"""iniciar red"""
	net.start()
	"""apertura de la cli"""
	IPCLI(net)
finally:
	"""detener red"""
	net.stop()
