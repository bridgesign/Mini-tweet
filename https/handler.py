# File for handling header

from time import gmtime, strftime, time

HEADER_SIZE = 8192


def set_time(t=None):
	return strftime("%a, %d %b %Y %X GMT", gmtime(t))


class httprequest:
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr

	def handle(self):
		data = self.conn.recv(HEADER_SIZE).decode()
		headers = {}
		k = data.find('\n\n')
		header = data[:k]
		body = data[k+1:]

		header = header.split('\n')

		method, url, ver = header[0].split()
		ver = ver[3:]

		for h in header:
			t =  h.find(':')
			headers[h[:t].lower()] = h[t+1:]

		if 'content-length' in headers:
			body += self.conn.revc(int(headers['content-length'])-len(body))

		if 'connection' in headers:
			headers['connection'] = True if headers['connection']=='keep-alive' else False
		else:
			headers['connection'] = False

		if 'cookie' in headers:
			headers['cookie'] = [tuple(c.split('=')) for c in headers['cookie'].split('; ')]

		headers['method'] = method
		headers['url'] = '/'.join(filter(lambda a: a!= '', url.replace('\\','/').split('/')))
		headers['HTTP'] = 1.1

		self.headers = headers
		self.body = body


# TODO: Change header response and modify headers for better performance
# TODO: Add cookie support
class httpresponse:
	def __init__(self, request, response, code):
		self.request = request
		self.response = response
		self.code = code

	def handle(self):
		res = ''
		res+='HTTP/{} {} {}\n'.format(self.request.headers['HTTP'], self.code, 'OK')
		res+='Date: {}\n'.format(set_time())
		res+='Content-type: text/html\n'
		res+='Content-Length: {}\n\n'.format(len(self.response))
		res+=self.response
		self.request.conn.send(res.encode())
