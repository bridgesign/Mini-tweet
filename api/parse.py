from . import schema

class parser:
	def __init__(self, obj=None, *args, **kwargs):
		self.obj = obj

		# Edit according to need
		self.schema = {
		'Query':schema.Query,
		'Mutation': schema.Mutation,
		'Subscription':schema.Subscription,
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
				if isinstance(response[r], schema.Error):
					return response[r]
			elif isinstance(r,dict):
				k, v = r.items()
				tobj = getattr(obj, k)()
				response[k] = self.resolve(ctx, tobj, v[0], v[1])
				if isinstance(response[k], schema.Error):
					return response[k]
			else:
				k, trets = r
				tobj_ls = getattr(obj, k)()
				resps = []
				for tobj in tobj_ls:
					r = self.resolve(ctx, tobj, {}, trets)
					if isinstance(r, schema.Error):
						return r
					resps.append(r)
				response[k] = resps
		return response

	def parse(self, ctx, query):
		schem = list(query.keys())[0]
		method = list(query[schem].keys())[0]
		args, rets = query[schem][method]
		schem = self.schema[schem](self.obj)
		method = getattr(schem, method)
		r = self.resolve(ctx, method, args, rets)
		if isinstance(r, schema.Error):
			response = r
		else:
			response = {'data':r}
		return response