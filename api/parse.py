from . import schema

class parser:
	def __init__(self, obj=None, *args, **kwargs):
		self.obj = obj

		# Edit according to need
		self.schema = {
		'Query':schema.Query,
		'Mutation': schema.Mutation,
		}

	def resolve(self, ctx, method, args, rets):
		obj = method(ctx ,**args)
		response = {}
		if isinstance(obj, (dict, str, list)):
			if isinstance(rets, str):
				return {rets:obj}
			else:
				return obj
		elif isinstance(obj, schema.Error):
			return obj.repr()
		for r in rets:
			if isinstance(r, str):
				response[r] = getattr(obj, r)()
			elif isinstance(r,dict):
				k, v = r.items()
				tobj = getattr(obj, k)()
				response[k] = self.resolve(ctx, tobj, v[0], v[1])
			else:
				k, trets = r
				tobj_ls = getattr(obj, k)()
				response[k] = [self.resolve(ctx, tobj, {}, trets) for tobj in tobj_ls]
		return response

	def parse(self, ctx, query):
		schem = list(query.keys())[0]
		method = list(query[schem].keys())[0]
		args, rets = query[schem][method]
		schem = self.schema[schem](self.obj)
		method = getattr(schem, method)
		response = {'data':self.resolve(ctx, method, args, rets)}
		return response