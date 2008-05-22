from django import template

register = template.Library()

def url_id(model):
    return model.key().id()


register.filter('url_id', url_id)
