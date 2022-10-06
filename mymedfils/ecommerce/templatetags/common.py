from django import template
from mymedfils import helpers
from products.models import Category, Brand
from carts.models import Cart, CartItem
from consultation.models import Country, State, City

register = template.Library()


@register.simple_tag
def multiply(first, second, *args, **kwargs):
    return first*second


@register.simple_tag
def get_categories_list(**kwargs):
    count = kwargs.get('count', '')
    if count != '':
        return Category.objects.all()[:count]
    return Category.objects.all()    

@register.simple_tag
def get_brands_list(**kwargs):
    count = kwargs.get('count', '')
    if count != '':
        return Brand.objects.all()[:count]
    return Brand.objects.all()

@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)

@register.simple_tag
def setvar(val=None):
    return val

@register.simple_tag
def get_cartcount(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is not None:
        cart_obj = Cart.objects.get(pk=cart_id)
        return cart_obj.cartitem_set.count()
    return 0

@register.simple_tag
def get_cities(**kwargs):
    return City.objects.all()

@register.simple_tag
def get_states(**kwargs):
    return State.objects.all()

@register.simple_tag
def get_countries(**kwargs):
    return Country.objects.all()

@register.simple_tag
def status_color(status):
    
    statuses = ['canceled','complete','success']
    if status not in statuses:
        status = 'other'

    return {
        'canceled':'#f02123',
        'complete':'#86b953',
        'success':'#86b953',
        'other': '#000000'
    }[status]


#Coupon amount
@register.simple_tag
def coupon_amount(cart_obj, total):
    return helpers.get_coupon_amount(cart_obj, total)

#Add two numbers
@register.simple_tag
def add_float(a, b):
    return float(a)+float(b)