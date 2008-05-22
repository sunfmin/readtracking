from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, Google App Engine with Django")
