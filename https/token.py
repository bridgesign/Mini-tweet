from .settings import secret
import hashlib
from time import time

def create_token(data, expire):
	s = ''
	for k,v in data.items():
		s+='{}:{}'.format(k,v)
	s+=';{}'.format(time()+expire)
	key = s+';{}'.format(secret)
	s+=';{}'.format(hashlib.md5(key.encode('utf-8')).hexdigest())
	return s

def validate_token(token):
	parts = token.split(';')
	mdhash = parts[-1]
	if float(parts[-2])<time():
		return {}
	check = hashlib.md5(str(';'.join(parts[:-1])+';{}'.format(secret)).encode('utf-8')).hexdigest()
	if check!=parts[-1]:
		return {}
	data = {}
	for p in parts[:-2]:
		k,v = p.split(':')
		data[k] = v
	return data