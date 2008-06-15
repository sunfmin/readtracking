from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from tracking.models import *

def login_required(func, request=None):
    def decorate(request, *args, **kws):
        user = users.get_current_user()
        if not user:
            if request.GET['url']:
                redirect_url = request.GET['url']
            if not redirect_url:
                redirect_url = request.get_full_path()
            html = "<a href=\"%s\" target=\"_top\">Please sign in your google account to use it</a>." % users.create_login_url(redirect_url)
            return HttpResponse(html)
        return func(request, *args, **kws)
    return decorate

@login_required
def myhome(request):
    quests = Quest.all().filter("creator = ", users.get_current_user()).order("-updated_at").fetch(100)
    return render_to_response('myhome.html', {"quests": quests})

@login_required
def ask(request):
    quest = Word.quest(url=request.GET['url'], word_name=request.GET['q'], title=request.GET['title'])
    return render_to_response('word.html', {"quest": quest, "dictionaries": Dictionary.my_dictionaries()})

@login_required
def dicts(request):
    if request.method == 'POST':
        MyDictionary.add_my_dic(url_template=request.POST['url_template'], title=request.POST['title'])
    return render_to_response('dicts.html', {"dictionaries": Dictionary.public_dictionaries(), "my_dictionaries": Dictionary.my_dictionaries()})

@login_required
def add_to_mydics(request, id=None):
    MyDictionary.add_my_dic(dic_id=id)
    return HttpResponseRedirect("/dicts")

@login_required
def remove_from_mydics(request, id=None):
    mydic = MyDictionary.get_by_id(int(id))
    if mydic:
        mydic.delete()
    return HttpResponseRedirect("/dicts")

@login_required
def my_dicts_update_order(request, id=None):
    if request.method == 'POST' and id and request.POST['order_priority']:
        mydic = MyDictionary.get_by_id(int(id))
        if mydic:
            mydic.order_priority = int(request.POST['order_priority'])
            mydic.put()
    return render_to_response('dicts_update_order.html', {"my_dictionaries": Dictionary.my_dictionaries()})


def index(request):
    return render_to_response('index.html', {})

def loader(request):
    return render_to_response('loader.js', {}, mimetype="application/javascript")


