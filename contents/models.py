from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import users

from string import *


DICTIONARIES = (
    Template("http://eow.alc.co.jp/${word}/UTF-8/"),
    Template("http://www.excite.co.jp/dictionary/english_japanese/?search=${word}&match=beginswith&dictionary=NEW_EJJE&block=38659&offset=254&title=${word}"),
)

class Word(db.Model):
    name = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def quest(cls, word_name, from_content):
        words = Word.all().filter('name =', word_name).fetch(1)

        if len(words) == 0:
            word = Word(
                name = word_name,
                creator=users.get_current_user()
            )
            word.put()
        else:
            word = words[0]

        for url_template in DICTIONARIES:
            content = Content.put_with_url(url_template.substitute(word=word_name), word)
            quest = Quest.put_with_word_and_content(content=from_content, word=word)

        return word

class Content(db.Model):
    text = db.TextProperty()
    url = db.StringProperty()
    explained_word = db.ReferenceProperty(Word)
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def put_with_url(cls, url, word=None):
        content_url = rstrip(url, "/")
        contents = Content.all().filter('url =', content_url).fetch(1)

        if len(contents) == 0:
            
            content = Content(
                url = url,
                text = db.Text(Stripper.strip_remote(url)),
                explained_word = word,
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
    def put_with_word_and_content(cls, word, content):
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

from urlparse import urlparse
# from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import re

  

class Stripper(db.Model):
    domain = db.StringProperty()
    url_path_regexp = db.StringProperty()
    priority = db.IntegerProperty()
    jquery_selector = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    @classmethod
    def strip_remote(cls, url):
        """docstring for strip_remote"""
        url_o = urlparse(url)
        domain = url_o.scheme + "://" + url_o.netloc
        path = replace(url, domain, "")
        
        fetched_content = urlfetch.fetch(url).content #.decode('utf-8')
        # clean_xhtml = BeautifulStoneSoup(fetched_content).prettify()
        
        strippers = Stripper.all().filter('domain = ', domain).order("-priority").fetch(100)
        for stripper in strippers:
            if re.compile(stripper.url_path_regexp).match(path):
                return fetched_content
        return fetched_content

