import re
from Handler import Handler
import Post
import Comment

from google.appengine.ext import db

class EditPost(Handler):
	'''
	This class if a child of PostPage handler and is for editing blog posts.
	'''

	def get(self, post_id):
		post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
		post = db.get(post_key)
		if not self.user:
			return self.redirect('/login')
		if not (self.user.name == post.creator):
			error = "Only the author of the post can edit this post."
			return self.render("permalink.html", post=post, error=error)
		return self.render('edit_post.html', post=post)



	def get_youtube(self,string):
		link = string.split("/")[3]
		try:
			if "//youtu.be" in link:
				youtube = youtube.replace("?", "&")
				vid_id, times = youtube.split("&")
				times = map(int, re.findall(r'\d', times))
				starting = 60 * times[0] + times[1]
				youtube = "%s?start=%s" % (vid_id, starting)
			else:
				youtube = link.split("=")[1]
			return youtube
		except IndexError:
			return False


	def post(self, post_id):
		post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
		post = db.get(post_key)

		if (self.request.get("change-title") or
			(self.request.get('change-content')) or
			(self.request.get('change-youtube'))):
			if post.creator == self.user.name:
				post.title = self.request.get('change-title')
				post.content = self.request.get("change-content")
				link = self.request.get("change-youtube")
				youtube = self.request.get('change-youtube')
				if not self.get_youtube(youtube):
					error = "Requires a valid Youtube URL"
					return self.render("edit_post.html", post=post, error=error)
				else:
					link = self.get_youtube(youtube)
					post.youtube = link
				post.put()
				return self.redirect("/")


		if (self.request.get("cancel_edit_post")):
			return self.redirect("/%s" % post_id)
