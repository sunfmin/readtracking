from django import template
from string import *
from google.appengine.api import users
from tracking.models import *
from django.utils import simplejson


register = template.Library()

def url_id(model):
    return model.key().id()

def show_word(quest):
    return quest.word.name

def dictionaries_json(quest):
    mydics = Dictionary.my_dictionaries()
    result = []
    for mydic in mydics:
        url_t = Template(mydic.dictionary.url_template)
        wordname = None
        if quest.word:
            wordname = quest.word.name
        try:
            url = url_t.substitute(url=quest.content.url, title=quest.content.title)
        except KeyError:
            if not wordname:
                continue
            url = url_t.substitute(word=wordname, url=quest.content.url, title=quest.content.title)

        result.append({'title': mydic.dictionary.title, 'url': url})
    return simplejson.dumps(result)

def greeting(any):
    user = users.get_current_user()
    if user:
      greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                  (user.nickname(), users.create_logout_url("/")))
    else:
      greeting = ("<a href=\"%s\">Sign in or register</a>." %
                  users.create_login_url("/my"))
    return greeting


register.filter('dictionaries_json', dictionaries_json)
register.filter('greeting', greeting)
register.filter('url_id', url_id)
register.filter('show_word', show_word)
