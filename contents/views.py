from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from contents.models import *

def index(request):
    contents = Content.all().fetch(100)
    return render_to_response('index.html', {"contents": contents})

def new(request):
    return render_to_response('new.html', {})

def create(request):
    content = Content.put_with_url(request.POST['content_url'])
    return HttpResponseRedirect('/contents/' + str(content.key().id()))

def show(request, id):
    content = Content.get_by_id(int(id))
    return render_to_response('show.html', {"content": content})

def quest(request, id, word):
    content = Content.get_by_id(int(id))
    Word.quest(word, content)
    return render_to_response('show.html', {"content": content})
def word(request, id):
    word = Word.get_by_id(int(id))
    return render_to_response('word.html', {"word": word})

