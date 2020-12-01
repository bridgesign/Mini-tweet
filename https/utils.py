from time import gmtime, strftime

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
