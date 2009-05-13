import os
from datetime import datetime

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp.util import run_wsgi_app

from models import *

template.register_template_library('templatefilters')

_DEBUG = True
class BaseRequestHandler(webapp.RequestHandler):
    """Supplies a common template generation function.

    When you call generate(), we augment the template variables supplied with
    the current user in the 'user' variable and the current webapp request
    in the 'request' variable.
    """
    def render(self, template_name, template_values={}):
        values = {
            'request': self.request,
            'user': users.get_current_user(),
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url('http://%s/' % (
                self.request.host,)),
            'debug': self.request.get('deb'),
            'application_name': 'Task Manager',}
        values.update(template_values)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))
        self.response.out.write(template.render(path, values, debug=_DEBUG))

class MyHome(BaseRequestHandler):
    @login_required
    def get(self):
        quests = Quest.all().filter("creator = ", users.get_current_user()).order("-updated_at").fetch(100)
        self.render('myhome.html', {"quests": quests})

class MyHomeMore(BaseRequestHandler):
    @login_required
    def get(self, before=None):
        before_time = datetime.strptime(before, "%Y%m%d%H%M%S")
        q = Quest.all()
        q.filter("creator = ", users.get_current_user())
        q.filter("updated_at < ", before_time)
        q.order("-updated_at")
        quests = q.fetch(100)
        self.render('quests.html', {"quests": quests})

class Ask(BaseRequestHandler):
    @login_required
    def get(self):
        word_name = self.request.GET.get('q', None)
        quest = Word.quest(url=self.request.GET.get('url', None), word_name=word_name, title=self.request.GET.get('title', None))
        self.render('word.html', {"quest": quest, "word_name": word_name, "dictionaries": Dictionary.my_dictionaries()})

class Dicts(BaseRequestHandler):
    @login_required
    def get(self):
        self.render('dicts.html', {"dictionaries": Dictionary.public_dictionaries(), "my_dictionaries": Dictionary.my_dictionaries()})

    def post(self):
        MyDictionary.add_my_dic(url_template=self.request.POST['url_template'], title=self.request.POST['title'])
        self.redirect('/dicts')

class AddToMyDicts(BaseRequestHandler):
    @login_required
    def get(self, id=None):
        MyDictionary.add_my_dic(dic_id=id)
        self.redirect("/dicts")

class RemoveFromMyDicts(BaseRequestHandler):
    @login_required
    def get(self, id=None):
        mydic = MyDictionary.get_by_id(int(id))
        if mydic:
            mydic.delete()
        self.redirect("/dicts")

class MyDictsUpdateOrder(BaseRequestHandler):
    def post(self, id=None):
        if id and self.request.POST['order_priority']:
            mydic = MyDictionary.get_by_id(int(id))
            if mydic:
                mydic.order_priority = int(self.request.POST['order_priority'])
                mydic.put()
        self.redirect("/dicts/update_order")

    @login_required
    def get(self):
        self.render('dicts_update_order.html', {"my_dictionaries": Dictionary.my_dictionaries()})

class Index(BaseRequestHandler):
    def get(self):
        self.render('index.html', {})

class Loader(BaseRequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/javascript'
        self.render('loader.js', {})

application = webapp.WSGIApplication([
    ('/ask', Ask),
    ('/myhome', MyHome),
    ('/myhome/before/(\d+)', MyHomeMore),
    ('/dicts/update_order/(.*)', MyDictsUpdateOrder),
    ('/dicts/update_order', MyDictsUpdateOrder),
    ('/dicts', Dicts),
    ('/mydics/add/(.*)', AddToMyDicts),
    ('/mydics/remove/(.*)', RemoveFromMyDicts),
    ('/loader.js', Loader),
    ('/', Index),
], debug=_DEBUG)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

