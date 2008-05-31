from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import users

from string import *


class Word(db.Model):
    name = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def quest(cls, url=None, word_name=None, title=None):
        if not word_name or len(strip(word_name)) == 0:
            return None
        # word_name = lower(word_name)
        from_content = Content.put_with_url(url, title=title)
        words = Word.all().filter('name =', word_name).fetch(1)

        if len(words) == 0:
            word = Word(
                name = word_name,
                creator=users.get_current_user()
            )
            word.put()
        else:
            word = words[0]

        Quest.put_with_word_and_content(word=word, content=from_content)
        return word

class Content(db.Model):
    text = db.TextProperty()
    url = db.StringProperty()
    title = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def put_with_url(cls, url, word=None, title=None):
        content_url = rstrip(url, "/")
        contents = Content.all().filter('url =', content_url).fetch(1)

        if len(contents) == 0:
            
            content = Content(
                url = url,
                title = title,
                creator=users.get_current_user()
            )
            content.put()
        else:
            content = contents[0]
        return content

    def excerpt(self):
        return ""

class Quest(db.Model):
    content = db.ReferenceProperty(Content)
    word = db.ReferenceProperty(Word)
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def put_with_word_and_content(cls, word=None, content=None):
        creator = users.get_current_user()
        quests_query = Quest.all()
        quests_query.filter('word = ', word)
        quests_query.filter('content = ', content)
        quests_query.filter('creator = ', creator)
        quests = quests_query.fetch(1)

        if len(quests) == 0:
            quest = Quest(
                word = word,
                content = content,
                creator=creator
            )
            quest.put()
        else:
            quest = quests[0]
        return quest
        
class Dictionary(db.Model):
    title = db.StringProperty()
    url_template = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def my_dictionaries(cls):
        alc = Dictionary(url_template="http://eow.alc.co.jp/${word}/UTF-8/",
                         title="ALC")
        goo = Dictionary(url_template="http://dictionary.goo.ne.jp/search.php?MT=${word}&kind=all&mode=0&kwassist=0",
                          title="Goo")
        return [goo, alc]

# 
# from urlparse import urlparse
# # from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
# import re
# 
#   
# 
# class Stripper(db.Model):
#     domain = db.StringProperty()
#     url_path_regexp = db.StringProperty()
#     priority = db.IntegerProperty()
#     jquery_selector = db.StringProperty()
#     creator = db.UserProperty()
#     created_at = db.DateTimeProperty(auto_now_add=True)
#     @classmethod
#     def strip_remote(cls, url):
#         url_o = urlparse(url)
#         domain = url_o.scheme + "://" + url_o.netloc
#         path = replace(url, domain, "")
#         
#         fetched_content = urlfetch.fetch(url).content.decode('utf-8')
#         # clean_xhtml = BeautifulStoneSoup(fetched_content).prettify()
#         
#         strippers = Stripper.all().filter('domain = ', domain).order("-priority").fetch(100)
#         for stripper in strippers:
#             if re.compile(stripper.url_path_regexp).match(path):
#                 return fetched_content
#         return fetched_content

