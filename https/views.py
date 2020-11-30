from . import handler
import os
from .settings import static
from . import settings
import json
from api.parse import parser
from . import token

import psycopg2
conn = psycopg2.connect("dbname=postgres user=postgres password=19954550")
cur = conn.cursor()

p = parser({'conn':conn, 'cur':cur})

def static_handler(request):
	split = request.headers['url'].split('/')
	filename, ftype = split[-1], split[-2]
	path = os.path.join(settings.static, ftype, filename)
	if os.path.isfile(path):
		with open(path, 'rb') as fp:
			data = fp.read()
	else:
		return handler.httpresponse(request, settings.NOT_FOUND_TEMPLATE, 404)
	h = handler.httpresponse(request, data, content_type=settings.ext_to_type[filename.split('.')[-1]])
	h.cache_control = ["public", "max-age=3600"]
	return h

def api_handler(request):
	if request.headers['method']=='POST':
		try:
			if 'token' in request.headers['cookie']:
				ctx = token.validate_token(request.headers['cookie']['token'])
			else:
				ctx = {}
			response = p.parse(ctx, json.loads(request.body))
			return handler.httpresponse(request, json.dumps(response), content_type='application/json')
		except:
			return handler.httpresponse(request, settings.BAD_REQUEST_TEMPLATE, 400)
	else:
		return handler.httpresponse(request, settings.BAD_REQUEST_TEMPLATE, 400)

def index(request):
	path = os.path.join('templates','index.html')
	with open(path, 'rb') as fp:
		data = fp.read()
	return handler.httpresponse(request, data)

patterns = (
	('^(?![\s\S])', index),
	('index(\.html|\.htm)?', index),
	('static/(image|css|js)/.*', static_handler),
	('api', api_handler)
	)
