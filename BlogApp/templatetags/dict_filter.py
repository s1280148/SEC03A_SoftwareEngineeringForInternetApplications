from django import template

register = template.Library()

@register.filter
def get_num_value(dictionary, key):
    value = int()

    try:
        value = dictionary.get(key)
    except KeyError:
        value = 0

    return value