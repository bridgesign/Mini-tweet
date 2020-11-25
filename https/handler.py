# File for handling header

from time import gmtime, strftime, time

HEADER_SIZE = 8192

code_msg = {
	200: 'OK',
	404: 'Not Found',
	413: 'Too Long Header',
	400: 'Bad Request',
}

def set_time(t=None):
	return strftime("%a, %d %b %Y %X GMT", gmtime(t))


class httpcookie:
	def __init__(self, key, value, expires=None, options = {}):
		self.key = key
		self.value = value
		self.expires = expires
		self.options = options

	def repr(self):
		parts = [(key, value)]
		if expires!= None:
			parts.append("expires={}".format(set_time(self.expires)))
		for k,v in options.items():
			if v==None:
				parts.append(k)
			else:
				parts.append("{}={}".format(k,v))
		return '; '.join(parts)


# TODO: Regex based splitting -  handling \r\n or \n
class httprequest:
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def handle(self):
		data = self.conn.recv(HEADER_SIZE).decode()
		self.headers = {'HTTP':1.0}
		k = data.find('\r\n\r\n')

		header = data[:k]
		body = data[k+4:]

		header = header.split('\r\n')

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
			body += self.conn.revc(int(self.headers['content-length'])-len(body))

		if 'connection' in self.headers:
			self.headers['connection'] = True if self.headers['connection']=='keep-alive' else False
		else:
			self.headers['connection'] = True

		if 'cookie' in self.headers:
			self.headers['cookie'] = [tuple(c.split('=')) for c in self.headers['cookie'].split('; ')]

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
		res.append('HTTP/{} {} {}'.format(self.request.headers['HTTP'], self.code, code_msg[self.code]))
		res.append('Date: {}'.format(set_time()))
		res.append('Cache-Control: {}'.format(', '.join(self.cache_control)))
		for c in self.cookies:
			res.append('Set-Cookie: {}'.format(c.repr()))
		if self.response:
			res.append('Content-type: {}'.format(self.content_type))
			res.append('Content-Length: {}\r\n'.format(len(self.response)))
			res.append(self.response)
		self.request.conn.send('\r\n'.join(res).encode())
