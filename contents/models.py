from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import users

class Content(db.Model):
    text = db.TextProperty()
    url = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_by_fetch(cls, url):
        content = Content(
            url = url,
            text = db.Text(urlfetch.fetch(url).content),
            creator=users.get_current_user()
        )
        content.put()
        return content

    def excerpt(self):
        return ""
