from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from tracking.models import *

def login_required(func, request=None):
    def decorate(request, *args, **kws):
        user = users.get_current_user()
        if not user:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
        return func(request, *args, **kws)
    return decorate

@login_required
def index(request):
    quests = Quest.all().fetch(100)
    return render_to_response('index.html', {"quests": quests})

@login_required
def ask(request):
    word = Word.quest(url=request.GET['url'], word_name=request.GET['q'], title=request.GET['title'])
    return render_to_response('word.html', {"word": word, "dictionaries": Dictionary.my_dictionaries()})

def loader(request):
    return render_to_response('loader.js', {}, mimetype="application/javascript")


