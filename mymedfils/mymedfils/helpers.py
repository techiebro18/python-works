import base64
from django.utils.text import slugify
import random
import string
import uuid 
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from ecommerce.models import PaymentMethod, Zipcode


def encode_str(string):
    message = string
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode_str(string):
    base64_message = string
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    print(slug)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def newOrderId():
    return uuid.uuid4().hex[:6].upper()

#Get percent
def get_percent(params):
    sale_price = float(params.get('sale_price', 0))
    price = params['price']
    result = {}
    if sale_price > 0 and sale_price < price:
        diff = price - sale_price
        percent = (diff/price)*100
        result['percent'] = percent
        result['percent_html'] = '<div class="_1fKPr">{}% OFF</div>'.format(percent)
    
    return result


# All emails
def get_emails(name):
    return {
        'admin':'atifahmad911@gmail.com'
    }[name]


def send_email(data, template_name='enquiry-mail.html', files={}):
    
    context = {
        'params': data
    }
    msg = render_to_string('emails/' + template_name, context)
    email = EmailMessage(
        data['subject'],
        msg,
        'abc@gmail.com',
        data['toEmails']
    )
    email.content_subtype = "html"
    #filePath = settings.BASE_DIR / 'static/consultation_files/Appointment_Letter_Atif_Ahmad.pdf'
    
    if files:
        for f in files:
            email.attach(f.name, f.read(), f.content_type)

    email.send(fail_silently=True)


#Get coupon amount
def get_coupon_amount(cart_obj, total):
    coupon_obj = cart_obj.coupon
    amount = None
    if coupon_obj is not None:
        if coupon_obj.is_percent:
            percent = coupon_obj.amount
            amount = ( total * percent ) / 100
        else:
            amount = coupon_obj.amount
    
        #total = float(total) - float(amount)
    return amount


#Check cart product quantity 
def check_order_quantity(cart):
    items = cart.cartitem_set.all()
    result = {}
    result['allow'] = True
    for item in items:
        if item.quantity > item.product.quantity:
            result['allow'] = False
            break
    
    return result


#Decrease cart product quantity
def decrease_order_quantity(cart):
    items = cart.cartitem_set.all()
    for item in items:
        product = item.product
        new_qty = int(product.quantity) - int(item.quantity)
        product.quantity = new_qty
        product.save()
        
    return cart

#Get payment methods by zipcode
def get_payment_methods_by_zipcode(zipcode=None):
    if zipcode is not None:
        try:
            zip_obj = Zipcode.objects.get(zipcode=zipcode)
            if zip_obj.cod:
                return PaymentMethod.objects.all()
            else:
                return PaymentMethod.objects.all().exclude(pk=1)
        except Zipcode.DoesNotExist:
            return PaymentMethod.objects.all()
    else:
        return PaymentMethod.objects.all()

#Get delivery charge by zipcode
def get_shipping_info_by_zipcode(zipcode=None):
    try:
        zip_obj = Zipcode.objects.get(zipcode=zipcode)
        return zip_obj.delivery_charge
    except Zipcode.DoesNotExist:
        return True