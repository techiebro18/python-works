from mymedfils import helpers
from django import template

register = template.Library()

@register.simple_tag
def encode_tag(string):
    return helpers.encode_str(string)


@register.simple_tag
def decode_tag(string):
    return helpers.decode_str(string)



