from django import template

register = template.Library()
@register.filter(name='private')
def private(dic, key):
    return dic[key]