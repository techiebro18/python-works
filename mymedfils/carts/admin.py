from django.contrib import admin
from .models import Cart, CartItem, Coupon

# Register your models here.

""" admin.site.register(Cart)
admin.site.register(CartItem)
 """
class CartItemAdmin(admin.StackedInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemAdmin]

    class Meta:
        model = Cart


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    pass


# Register coupon
admin.site.register(Coupon)