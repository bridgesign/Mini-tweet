from . import schema

class parser:
	def __init__(self, obj=None, *args, **kwargs):
		self.obj = obj

		# Edit according to need
		self.schema = {
		'Query':schema.Query,
		'Mutation': schema.Mutation,
		}

	def resolve(self, method, args, rets):
		obj = method(**args)
		response = {}
		for r in rets:
			if not isinstance(r, dict):
				response[r] = getattr(obj, r)()
			else:
				k, v = r.items()
				tobj = getattr(obj, k)()
				response[k] = self.resolve(tobj, v[0], v[1])
		return response

	def parse(self, query):
		schem = list(query.keys())[0]
		method = list(query[schem].keys())[0]
		args, rets = query[schem][method]
		schem = self.schema[schem](self.obj)
		method = getattr(schem, method)
		response = {'data':self.resolve(method, args, rets)}
		return response