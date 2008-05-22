from google.appengine.ext import db
class Content(db.Model):
  text = db.TextProperty()
  creator = db.UserProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)

