from django.urls import path, include
from . import views
from carts import views as cart_views


app_name = 'ecommerce'

urlpatterns = [
    path('', views.welcome, name='home'),
    path('category/<slug>/', views.products_by_category, name='products_by_category'),
    path('brand/<slug>/', views.products_by_brand, name='products_by_brand'),
    path('product/<slug>/', views.product_details, name='product_details'),
    path('add-to-cart/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/', cart_views.cart, name='cart'),
    path('update_cart/', cart_views.update_cart, name='update_cart'),
    path('delete_cart/', cart_views.delete_cart, name='delete_cart'),
    path('checkout/', cart_views.checkout, name='checkout'),
    path('ajax-shipping-checkout/', cart_views.ajax_shipping_checkout, name='ajax_shipping_checkout'),
    path('place-order/', cart_views.place_order, name='place_order'),
    path('thank-you/', views.thankyou, name='thankyou'),
    path('apply-coupon/', cart_views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', cart_views.remove_coupon, name='remove_coupon'),
    path('signup/', views.user_registration, name='user_registration'),
    path('signin/', views.signin_form, name='signin_form'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('my-account/', views.myaccount_form, name='myaccount_form'),
    path('my-address/', views.my_address, name='my_address'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<order_id>', views.order_details, name='order_details'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/<email>', views.reset_password, name='reset_password'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('page/<slug>/', views.page, name='page'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('check_delivery_zip/', views.check_delivery_by_zipcode, name='check_delivery_by_zipcode'),
    path('get_city_by_zipcode/', views.get_city_by_zipcode, name='get_city_by_zipcode'),
    path('payment/<order_id>/', cart_views.payment, name='payment'),
    path('payment_success/', cart_views.payment_success, name='payment_success'),
    #path('custom-sitemap.xml', views.custom_sitemap, name="custom_sitemap"),
    path('ajax-payment-methods/', cart_views.ajax_payment_methods_by_zipcode, name='ajax_payment_methods'),
    path('ajax-shipping-methods/', cart_views.ajax_shipping_methods_by_zipcode, name='ajax_shipping_methods'),
    path('clear-cache/', views.clear_cache, name='clear_cache')
]
