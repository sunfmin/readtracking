from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import users

from string import *
from datetime import datetime


class Word(db.Model):
    name = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def quest(cls, url=None, word_name=None, title=None):
        if not word_name or len(strip(word_name)) == 0:
            return None
        # word_name = lower(word_name)
        from_content = Content.put_with_url(url=url, title=title)
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
    def put_with_url(cls, url=None, word=None, title=None):
        url = rstrip(url, "/")
        contents = Content.all().filter('url =', url).fetch(1)

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
    updated_at = db.DateTimeProperty(auto_now_add=True)
    search_count = db.IntegerProperty()
    
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
        
        quest.updated_at = datetime.now()
        if not quest.search_count:
            quest.search_count = 1
        else:
            quest.search_count = quest.search_count + 1
        quest.put()
        
        return quest

class Dictionary(db.Model):
    title = db.StringProperty()
    url_template = db.StringProperty()
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def put_with_url_template(cls, url_template=None, title=None):
        url_template = rstrip(url_template, "/")
        dicts = Dictionary.all().filter('url_template =', url_template).fetch(1)

        if len(dicts) == 0:
            dictionary = Dictionary(
                url_template = url_template,
                title = title,
                creator=users.get_current_user()
            )
            dictionary.put()
        else:
            dictionary = dicts[0]
        return dictionary
    
    @classmethod
    def public_dictionaries(self):
        return Dictionary.all().fetch(100)


    @classmethod
    def my_dictionaries(cls):
        mydics = MyDictionary.all().filter('creator =', users.get_current_user()).fetch(100)
        return mydics

        # alc = Dictionary(url_template="http://eow.alc.co.jp/${word}/UTF-8/",
        #                  title="ALC")
        # goo = Dictionary(url_template="http://dictionary.goo.ne.jp/search.php?MT=${word}&kind=all&mode=0&kwassist=0",
        #                   title="Goo")
        # return [goo, alc]


class MyDictionary(db.Model):
    dictionary = db.ReferenceProperty(Dictionary)
    creator = db.UserProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_my_dic(cls, url_template=None, title=None, dic_id=None):
        if not dic_id and (not url_template or not strip(url_template)):
            return None
        if not dic_id:
            dic = Dictionary.put_with_url_template(url_template=url_template, title=title)
        else:
            dic = Dictionary.get_by_id(int(dic_id))
        if not dic:
            return None
        
        creator = users.get_current_user()
        mydicsq = MyDictionary.all()
        mydicsq.filter('dictionary = ', dic)
        mydicsq.filter('creator = ', creator)
        mydics = mydicsq.fetch(1)
        
        if len(mydics) == 0:
            mydic = MyDictionary(
                dictionary = dic,
                creator=creator
            )
            mydic.put()
        else:
            mydic = mydics[0]
        return mydic



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

