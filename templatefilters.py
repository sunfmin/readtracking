from google.appengine.ext.webapp import template
from google.appengine.api import users
from string import *
from models import *
from django.utils import simplejson


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
        content_url = None
        title = None
        if quest.content:
            content_url = quest.content.url
            title = quest.content.title
        try:
            url = url_t.substitute(url=content_url, title=title)
        except KeyError:
            if not wordname:
                continue
            url = url_t.substitute(word=lower(wordname), url=content_url, title=title)

        result.append({'title': mydic.dictionary.title, 'url': url})
    return simplejson.dumps(result)

def head_dictionary_template(any):
    return Dictionary.my_dictionaries()[0].dictionary.url_template

def greeting(any):
    user = users.get_current_user()
    if user:
      greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>) or to <a href='/myhome'>My Home</a>" %
                  (user.nickname(), users.create_logout_url("/")))
    else:
      greeting = ("<a href=\"%s\">Sign in or register</a>." %
                  users.create_login_url("/myhome"))
    return greeting

def last_updated_at(quests):
    return quests[-1].updated_at.strftime("%Y%m%d%H%M%S")

register = template.create_template_register()
register.filter(dictionaries_json)
register.filter(greeting)
register.filter(url_id)
register.filter(show_word)
register.filter(last_updated_at)
register.filter(head_dictionary_template)
