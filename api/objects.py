class User:
	def __init__(self, user_id):
		self.user_id = user_id

	def uid(self):
		return self.user_id


class Tweet:
	def __init__(self, user, hashtags, post):
		self.user = user
		self.hashtags = hashtags
		self.post = post