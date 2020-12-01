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

	def resolve(self, ctx, method, args, rets, obj=True):
		if obj:
			obj = method
		else:
			obj = method(ctx=ctx ,**args)
		response = {}
		if isinstance(obj, (dict, str)):
			if isinstance(rets, str):
				return {rets:obj}
			else:
				return obj
		elif isinstance(obj, schema.Error):
			return obj.repr()
		elif not isinstance(rets, (tuple, list)):
			rets = (rets,)
		for r in rets:
			if isinstance(r, str):
				response[r] = getattr(obj, r)()
				if isinstance(response[r], schema.Error):
					return response[r]
			elif isinstance(r,dict):
				[(k, v)] = r.items()
				tobj = getattr(obj, k)()
				response[k] = self.resolve(ctx, tobj, {}, v)
				if isinstance(response[k], schema.Error):
					return response[k]
			else:
				k, trets = r
				resps = []
				for tobj in obj:
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
		r = self.resolve(ctx, method, args, rets, obj=False)
		if isinstance(r, schema.Error):
			response = r
		else:
			response = {'data':r}
		return response