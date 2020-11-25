from . import handler
import os
from .settings import static
from . import settings

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
	h.cache_control = ["public"]
	return h


def index(request):
	return handler.httpresponse(request, '<html><head><link rel="stylesheet" href="static/css/test.css"></head>index</html>')

patterns = (
	('^(?![\s\S])', index),
	('index(\.html|\.htm)?', index),
	('static/(image|css|js)/.*', static_handler),
	)
