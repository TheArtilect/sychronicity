from Handler import Handler
import Post
import Comment

from google.appengine.ext import db

class EditPost(Handler):
	'''

	'''
	def get(self, post_id):
		post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
		post = db.get(post_key)
		likes = len(post.likes)
		return self.render('edit_post.html', post=post, likes=likes)

# class EditPost(Handler):
# 	"""
# 	This class if a child of PostPage handler and is for editing blog posts.
# 	"""
#
# 	def get(self, post_id):
# 		post_key = db.Key.from_path("Post", int(post_id),
#                                     parent=Post.blog_key())
#         post = db.get(post_key)
#
#         likes_list = post.likes
#
#         likes = len(post.likes)
#
# 		self.render('edit_post.html', post=post, likes = likes, comments = comments)
#
#         # if not self.user:
#         # 	return self.redirect("/login")
#         # elif not (self.user == post.creator):
#         # 	self.write("Only the author of the comment can edit this post.")
#         # 	return
#     	# else:
# 	    #     comments = get_comments(post_id)
# 	    #     return self.render("edit_post.html",
# 		# 		        	post = post,
# 		# 		        	likes = lies,
# 		# 		        	comments = comments)
#
#
#
#
# 	def post(self, post_id):
# 		post_key = db.Key.from_path("Post", int(post_id),
#                                     parent=Post.blog_key())
#
#         post = db.get(post_key)
#
#         edit_post = False
#
#         if self.request.get('edit'):
#             if (post.creator == self.user):
#                 edit_post = True
#             else:
#                 error = "Only the author can edit this post!"
#
#
#         if (self.request.get("change-title")) or (self.request.get("change-content")):
#             if post.creator == self.user:
#                 post.title = self.request.get("change-title")
#                 post.content = self.request.get("change-content")
#                 post.put()
#                 edit_post = False
#                 return self.redirect("/")
#
#
#         if (self.request.get("cancel_edit_post")):
#             return self.redirect("/%s" % post_id)
