class User:
	def __init__(self, username, password):
		self.user = username
		self.passw = password

	def username(self):
		return self.user
	def password(self):
		return self.passw