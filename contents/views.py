from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from contents.models import *
import string

def index(request):
    contents = Content.all().fetch(100)
    return render_to_response('index.html', {"contents": contents})

def new(request):
    return render_to_response('new.html', {})


def create(request):
    content_url = request.POST['content_url']
    content_url = string.rstrip(content_url, "/")
    contents = Content.all().filter('url =', content_url).fetch(1)

    if len(contents) == 0:
        content = Content.create_by_fetch(content_url)
    else:
        content = contents[0]

    return HttpResponseRedirect('/contents/' + str(content.key().id()))

def show(request, id):
    content = Content.get_by_id(int(id))
    return render_to_response('show.html', {"content": content})
