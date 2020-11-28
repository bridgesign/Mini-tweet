from .objects import User
from https import token

class Error:
	def __init__(self, msg, code:int = 0):
		self.msg = msg
		self.code = code
	def repr(self):
		return {"Error":self.msg, "status":str(self.code)}

class Query:
	def __init__(self, obj=None):
		self.obj = obj

	def login(self, ctx, username:str, password:str):
		if username=='uu' and password=='pass':
			return token.create_token({'username':username}, 3600)
		else:
			return Error("Credential Error")

	def access(self, ctx):
		if 'username' in ctx:
			return User(ctx['username'])
		else:
			return Error("Not Logged In")


class Mutation:
	def __init__(self, obj=None):
		self.obj = obj