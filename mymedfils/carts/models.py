from django.db import models
from django.conf import settings
from products.models import Product
from datetime import datetime
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

# Create your models here.
class Coupon(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField()
    is_percent = models.BooleanField(default=False)
    expiry = models.DateField(blank=True, null=True)
    is_forever = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_ordered = models.BooleanField(default=False, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, blank=True, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    """ def __str__(self):
        return self.user.first_name """


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    """ def __str__(self):
        return self.product.name """
     




""" def calculate_cart_total(sender, instance, created, *args, **kwargs):
    
    cart_obj = instance.cart
    print("Instance: ", cart_obj)
    cart_items = cart_obj.cartitem_set.all()
    total = 0
    for item in cart_items:
        total += item.quantity*item.product.price

    newCartObj = Cart(id=cart_obj.id, subtotal=total, total=total)
    newCartObj.save()
 """
#post_save.connect(calculate_cart_total, sender=CartItem)


