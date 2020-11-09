import socket
from concurrent.futures import ThreadPoolExecutor
from . import handler
from . import views

class server:
	"""docstring for ClassName"""
	def __init__(self, host:str ='', port:int =8080, timeout:int =180, threads:int =10):
		self.port = port
		self.host = host
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.thread_pool = ThreadPoolExecutor(max_workers=threads)


	def handle(self, conn, addr):
		# Create request
		request = handler.httprequest(conn, addr)
		ret = request.handle()

		if ret:
			handler.httpresponse(request, '', ret).handle()
			conn.close()
			return

		for pattern in views.patterns:
			if request.headers['url'] == pattern[0]:
				pattern[1](request).handle()
				break
		else:
			response = "<html><body><h1>Not Found</h1></body></html>"
			code = 404
			handler.httpresponse(request, response, code).handle()

		conn.close()


	def serve(self):
		self.sock.bind((self.host, self.port))
		print("Starting Server on", self.port)
		self.sock.listen()
		while True:
			conn, addr = self.sock.accept()
			conn.settimeout(self.timeout)
			self.thread_pool.submit(self.handle, conn, addr)