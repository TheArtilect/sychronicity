from PostPage import PostPage

from google.appengine.ext import db


class EditPost(PostPage):
	"""
	This class if a child of PostPage handler and is for editing blog posts.
	"""

	def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), 
                                    parent=Post.blog_key())

        post = db.get(post_key)

        likes_list = post.likes

        likes = len(post.likes)

        if not self.user:
        	return self.redirect("/login")
        elif not (self.user == post.creator):
        	self.write("Only the author of the comment can edit this post.")
        	return
    	else:
	        comments = get_comments(post_id)
	        self.render("edit_post.html", 
				        	post = post,
				        	likes = lies,
				        	comments = comments)




	def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())

        post = db.get(post_key)

        edit_post = False

        if self.request.get('edit'):
            if (post.creator == self.user):
                edit_post = True
            else:
                error = "Only the author can edit this post!"


        if (self.request.get("change-title")) or (self.request.get("change-content")):
            if post.creator == self.user:
                post.title = self.request.get("change-title")
                post.content = self.request.get("change-content")
                post.put()
                edit_post = False
                self.redirect("/")


        if (self.request.get("cancel_edit_post")):
            self.redirect("/%s" % post_id)


