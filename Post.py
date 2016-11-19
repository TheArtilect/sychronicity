
from google.appengine.ext import db


class Post(db.Model):
    """
    This class is for blog posts
    Attributes:
        title (str):  Title of post.
        content (str): Content of the post.
        youtube (str): Youtube video id.
        creator (str): Author of the post.
        created (date): Date of when the blog post was created.
        last_modified (date): Date of when the blog post was last modified.
        likes (list): List of strings of blog users that liked the blog post.
        comments (list): List of strings of comment key ids of the blog post.
    """


    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    youtube = db.StringProperty()
    creator = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    likes = db.StringListProperty()
    comments = db.StringListProperty()


    def rendered_content(self):
        """
        rendered_content:  Method for retaining the multiline format of the
                            blogpost.

        Returns:
            String of blog post content with newlines replaced with html breaks.
        """
        return self.content.replace("\n", "<br>")


    def render_back(self):
        """
        render_back:  Method for retaining the multiline format of the
                        blogpost after it has been retrieved from the database.
        Returns:
            String of blog post content with html breaks replaced with newlines.
        """
        return self.content.replace("<br>", "\n")


    def number_of_likes(self):
        """
        number_of_likes:  Method for getting the number of likes of a blog post.
        Returns:
            Integer of the number of blog post likes.
        """
        return len(self.likes)


    def number_of_comments(self):
        """
        number_of_comments:  Method for getting the number of likes of a blog
                                post.
        Returns:
            Integer of the number of blog comments.
        """
        return len(self.comments)


def blog_key(name = 'default'):
    return db.Key.from_path('/', name)
