class User:
	def __init__(self, username):
		self.user = username

	def username(self):
		return self.user

class Tweet:
	def __init__(self, user, hashtags, post):
		self.user = user
		self.hashtags = hashtags
		self.post = post