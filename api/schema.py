from .user import User

class Query:
	def __init__(self, obj=None):
		self.obj = obj

	def login(self, username:str, password:str):
		return User(username, password)


class Mutation:
	def __init__(self, obj=None):
		self.obj = obj