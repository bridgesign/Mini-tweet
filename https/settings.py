import os

HEADER_SIZE = 8192

code_msg = {
	200: 'OK',
	404: 'Not Found',
	413: 'Too Long Header',
	400: 'Bad Request',
}

NOT_FOUND_TEMPLATE = "<html><body><h1>Not Found</h1></body></html>"


ext_to_type = {
	'png':'image/png',
	'gif':'image/gif',
	'jpg':'image/jpeg',
	'tiff':'image/tiff',
	'css':'text/css',
}

static = 'static'