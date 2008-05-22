from django import template

register = template.Library()

def url_id(model):
    return model.key().id()

def show_word(quest):
    return quest.word.name


register.filter('url_id', url_id)
register.filter('show_word', show_word)
