import socket
from concurrent.futures import ThreadPoolExecutor
from . import handler
from . import views
import re
from .settings import NOT_FOUND_TEMPLATE

class server:
	"""docstring for ClassName"""
	def __init__(self, host:str ='', port:int =8080, timeout:int =60, threads:int =10):
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
			if bool(re.match(pattern[0], request.headers['url'])):
				pattern[1](request).handle()
				break
		else:
			handler.httpresponse(request, NOT_FOUND_TEMPLATE, 404).handle()

		if request.headers['connection']:
			try:
				self.handle(conn, addr)
			except:
				conn.close()
		else:
			conn.close()


	def serve(self):
		self.sock.bind((self.host, self.port))
		print("Starting Server on", self.port)
		self.sock.listen()
		while True:
			conn, addr = self.sock.accept()
			conn.settimeout(self.timeout)
			self.thread_pool.submit(self.handle, conn, addr)