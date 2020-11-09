from . import handler

def index(request):
	return handler.httpresponse(request, "index")

patterns = (
	('', index),
	)
