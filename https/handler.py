# File for handling header

from .settings import HEADER_SIZE, code_msg
import re
from .utils import set_time

class httprequest:
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def handle(self):
		data = self.conn.recv(HEADER_SIZE).decode()
		self.headers = {'HTTP':1.0}
		k = re.search('\r\n\r\n|\n\n', data)

		header = data[:k.span()[0]]
		body = data[k.span()[1]:]

		header = re.split('\r\n|\n', header)

		try:
			method, url, ver = header[0].split()
		except:
			return 400

		if k==-1:
			return 413

		ver = ver[3:]

		for h in header:
			t =  h.find(':')
			self.headers[h[:t].lower()] = h[t+1:].strip()

		if 'content-length' in self.headers:
			body += self.conn.recv(int(self.headers['content-length'])-len(body)).decode()

		if 'connection' in self.headers:
			self.headers['connection'] = True if self.headers['connection']=='keep-alive' else False
		else:
			self.headers['connection'] = True

		if 'cookie' in self.headers:
			cooks = self.headers['cookie'].split('; ')
			self.headers['cookie'] = {}
			for c in cooks:
				k,v = c.split('=')
				self.headers['cookie'][k] = v
		else:
			self.headers['cookie'] = {}

		self.headers['method'] = method
		self.headers['url'] = '/'.join(filter(lambda a: a!= '', url.replace('\\','/').split('/')))
		self.headers['HTTP'] = 1.1

		self.body = body

		return 0


# TODO: Change header response and modify headers for better performance
class httpresponse:
	def __init__(self, request, response='', code:int =200, content_type:str ="text/html"):
		self.request = request
		self.response = response
		self.code = code
		self.cache_control = ["private"]
		self.cookies = []
		self.content_type = content_type

	def handle(self):
		if self.response==None:
			return
		res = []
		res.append('HTTP/{} {} {}'.format(self.request.headers['HTTP'], self.code, code_msg[self.code]).encode())
		res.append('Date: {}'.format(set_time()).encode())
		res.append('Cache-Control: {}'.format(', '.join(self.cache_control)).encode())
		for c in self.cookies:
			res.append('Set-Cookie: {}'.format(c.repr()).encode())
		res.append('Content-type: {}'.format(self.content_type).encode())
		res.append('Content-Length: {}\r\n'.format(len(self.response)).encode())
		if self.response:
			if isinstance(self.response, str):
				res.append(self.response.encode())
			else:
				res.append(self.response)
		else:
			res.append(b'')
		self.request.conn.sendall(b'\r\n'.join(res))
