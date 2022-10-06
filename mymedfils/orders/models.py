from django.db import models
from carts.models import Cart
from django.conf import settings
from ecommerce.models import ShippingMethod, PaymentMethod
from datetime import datetime

User = settings.AUTH_USER_MODEL

ORDER_CHOICES = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('inprogress', 'In Progress'),
    ('complete', 'Complete'),
    ('canceled', 'Canceled'),
]
# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=60, decimal_places=2)
    total = models.DecimalField(max_digits=60, decimal_places=2)
    status = models.CharField(choices=ORDER_CHOICES, default='pending', max_length=10)
    
    billing_name = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.EmailField(max_length=255, blank=True, null=True)
    billing_mobile = models.CharField(max_length=12, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_postcode = models.CharField(max_length=6, blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.CharField(max_length=100, blank=True, null=True)
    
    shipping_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_email = models.EmailField(max_length=255, blank=True, null=True)
    shipping_mobile = models.CharField(max_length=12, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_postcode = models.CharField(max_length=6, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_country = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(default=datetime.now )

    def __str__(self):
        return '#{}'.format(self.order_id)


    @property
    def quantity(self):
        items = self.cart.cartitem_set.all()
        total = 0
        for item in items:
            total += item.quantity
        return total

        

class Payment(models.Model):
    order_id = models.CharField(max_length=50)
    razorpay_payment_id = models.CharField(max_length=200)
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_signature = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)