import socket
import threading
from . import handler
from . import views

class server:
	"""docstring for ClassName"""
	def __init__(self, host='', port=8080, timeout=180):
		self.port = port
		self.host = host
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def handle(self, conn, addr):
		# Create request
		request = handler.httprequest(conn, addr)
		request.handle()
		for pattern in views.patterns:
			if request.headers['url'] == pattern[0]:
				response, code = pattern[1](request)
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
			threading.Thread(target=self.handle, args=(conn, addr)).start()