from django.contrib import admin
from .models import Order, Payment

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'billing_name', 'billing_email', 'billing_mobile', 'status', 'created_at']

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature', 'created_at']

    class Meta:
        model = Payment


admin.site.register(Payment, PaymentAdmin)


