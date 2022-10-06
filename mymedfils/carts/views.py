from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Cart, CartItem, Coupon
from products.models import Product
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.core import serializers
from ecommerce.models import ShippingMethod, PaymentMethod
#from mymedfils import helpers
from orders.models import Order, Payment
from django.contrib import messages
from datetime import datetime, date
from mymedfils.helpers import send_email, get_emails, check_order_quantity, decrease_order_quantity, get_payment_methods_by_zipcode, get_shipping_info_by_zipcode
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def add_to_cart(request):
    if request.method == 'POST': 
        # Get cart id from session if doesn't exist create a new one with user/anonymous if logged in assign anonymous = current user
        # If cart exist add product item into it.
        #del request.session['cart_id'] 

        cart_id = request.session.get('cart_id')
        pid = request.POST['pid']
        quantity = request.POST['quantity']
        

        current_user    = request.user
        if not current_user.is_authenticated:
            current_user = None

        
        if cart_id is None:
            cart_object = Cart.objects.create(user=current_user)
            cart_id = cart_object.id
            request.session['cart_id'] = cart_id
        else:
            cart_object     = Cart(id=cart_id, user=current_user)
            cart_object.save()

        #print("cart_id: ", cart_id)
        # Create cart item if already does not exist
        cart_items = cart_object.cartitem_set.all()
        product_obj = Product.objects.get(pk=pid)
        if cart_items.count() > 0:
            f = 0
            for item in cart_items:
                if int(pid) == int(item.product_id):
                    f = 1
                    break

            #if product is not in the cart
            if f != 1:
                cart_item_obj = CartItem.objects.create(cart=cart_object, product=product_obj, quantity=quantity)
                
        else:
            cart_item_obj = CartItem.objects.create(cart=cart_object, product=product_obj, quantity=quantity)

        return HttpResponseRedirect(reverse('ecommerce:cart'))
    else:
        return HttpResponse('Http method is not allowed.')
    


def cart(request):
    cart_id = request.session.get('cart_id')
    
    # Assign logged in user to the cart, If user added product into cart and then logged in.
    user = request.user
    context = {}
    items = []
    total = 0
    try:
        if cart_id is not None:
            if user.is_authenticated:
                #cart_object = Cart(pk=cart_id, user=user)
                cart_object = Cart.objects.get(pk=cart_id)
                cart_object.user = user
                cart_object.save()
            else:
                cart_object = Cart.objects.get(pk=cart_id)
            
            items = cart_object.cartitem_set.all()
            """ for item in items:
                total += item.quantity*item.product.price """
            cart_dict = calculate_cart(cart_id)

            context['subtotal'] = cart_dict.get('sub_total', 0.00)
            context['total'] = cart_dict.get('total', 0.00)
            context['cart'] = cart_object
    
    except ObjectDoesNotExist:
        raise Http404('Cart id does not exist.')

    # Get all items of the cart and display using many to many relation.
    context['items'] = items

    #print("context: ", context)
    return render(request, 'carts/cart.html', context)


def update_cart(request):
    item_id = request.POST.get('item_id', None)
    item_obj = CartItem.objects.get(pk=item_id)
    quantity = request.POST.get('quantity', 1)
    item_obj.quantity = quantity
    item_obj.save()
    messages.success(request, 'Quantity updated successfully!')
    return HttpResponseRedirect(reverse('ecommerce:cart'))


def delete_cart(request):
    # Get particular item id and remove from cart
    item_id = request.POST['item_id']
    item_obj = CartItem.objects.get(pk=item_id)
    item_obj.delete()

    return HttpResponseRedirect(reverse('ecommerce:cart'))


def checkout(request):
    cart_id = request.session.get('cart_id')
    
    current_user = {}
    if request.user.is_authenticated:
        current_user = request.user

    if cart_id is None:
        return HttpResponseRedirect(reverse('ecommerce:cart'))
    

    #All shipping methods
    shipping_methods = ShippingMethod.objects.all()
    #All payment methods
    payment_methods = PaymentMethod.objects.all().exclude(pk=1)
    
    delivery_charge = True
    #Assign user to the cart
    if request.user.is_authenticated:
        """ cart_object = Cart(pk=cart_id, user=current_user)
        cart_object.save() """
        cart_object = Cart.objects.get(pk=cart_id)
        cart_object.user = current_user
        cart_object.save()

        #Payment methods by zipcode
        payment_methods = get_payment_methods_by_zipcode(current_user.profile.billing_postcode)
        delivery_charge = get_shipping_info_by_zipcode(current_user.profile.billing_postcode)
    else:
        cart_object = Cart.objects.get(pk=cart_id)

    #Get cart products
    products = cart_object.cartitem_set.all()
    
    
    #if form is submitted from checkout
    default_payment = {}
    default_shipping = {}
    if request.method == "POST":
        #Choosen shipping method on checkout page
        shipping_id = request.POST['shipping_method']
        shipping_obj = ShippingMethod.objects.filter(pk=shipping_id)
        if shipping_obj.count() > 0:
            default_shipping = shipping_obj[0]

        cart_dict = calculate_cart(cart_id, default_shipping=default_shipping)
    else:
        #if form is submitted from checkout
        #Default shipping method
        shipping_obj = ShippingMethod.objects.filter(default=True)
        #default_shipping = {}
        if shipping_obj.count() > 0:
            default_shipping = shipping_obj[0]

        #Get cart sub total
        total_subtotal_obj = calculate_cart(cart_id)
        sub_total = total_subtotal_obj.get('sub_total')
        shipping_methods = []
        if float(sub_total) >= float('1000') and delivery_charge != True:
            cart_dict = calculate_cart(cart_id, default_shipping=default_shipping)
            shipping_methods.append(default_shipping)
        else:
            default_shipping = ShippingMethod.objects.get(pk=2)
            cart_dict = calculate_cart(cart_id, default_shipping=default_shipping)
            shipping_methods.append(default_shipping)


    #Default payment method
    payment_obj = PaymentMethod.objects.filter(default=True)
    #default_payment = {}
    if payment_obj.count() > 0:
        default_payment = payment_obj[0]


    context = {
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods,
        'products': products,
        'default_shipping': default_shipping,
        'default_payment': default_payment,
        'cart_dict': cart_dict,
        'current_user': current_user,
        'cart_object': cart_object

    }  
    return render(request, "carts/checkout.html", context)



def ajax_shipping_checkout(request):
    if request.is_ajax and request.method == 'POST':
        shipping_id = request.POST.get('shipping_method')
        cart_id     = request.POST.get('cart_id')
        shipping_obj = ShippingMethod.objects.filter(pk=shipping_id)
        if shipping_obj.count() > 0:
            default_shipping = shipping_obj[0]

        cart_dict = calculate_cart(cart_id, default_shipping=default_shipping)
        #json_cart_dict = serializers.serialize('json', cart_dict)
        return JsonResponse({"data":cart_dict}, status=200)

    # some error occured
    return JsonResponse({"error": "Http Method not allowed"}, status=400)    

def ajax_payment_methods_by_zipcode(request):
    if request.is_ajax and request.method == 'POST':
        zipcode = request.POST.get('zipcode', None)
        payment_methods = get_payment_methods_by_zipcode(zipcode)
        response = {}
        html = ''
        i=1
        for payment in payment_methods:
            """ if payment.id == 1:
                html += '<div class="form-group"><input type="radio" name="payment_method" tabindex="1" id="payment_method_'+str(i)+'" class="control" value="'+str(payment.id)+'" checked="checked"> <label for="payment_method_'+str(i)+'" style="display: inline; cursor: pointer;"> '+payment.name+'</label></div>'
            else:
                html += '<div class="form-group"><input type="radio" name="payment_method" tabindex="1" id="payment_method_'+str(i)+'" class="control" value="'+str(payment.id)+'"> <label for="payment_method_'+str(i)+'" style="display: inline; cursor: pointer;"> '+str(payment.name)+'</label></div>' """


            html += '<div class="form-group"><input type="radio" name="payment_method" tabindex="1" id="payment_method_'+str(i)+'" class="control" value="'+str(payment.id)+'" checked="checked"> <label for="payment_method_'+str(i)+'" style="display: inline; cursor: pointer;"> '+str(payment.name)+'</label><br /><p>'+str(payment.description)+'</p></div>'
            i+=1 

        response['html'] = html
        response['message'] = 'Success'
        return JsonResponse(response)
        
    return JsonResponse({"error": "Http Method not Allowed"})

def ajax_shipping_methods_by_zipcode(request):
    if request.is_ajax and request.method == 'POST':
        zipcode = request.POST.get('zipcode', None)
        delivery_charge = get_shipping_info_by_zipcode(zipcode)

        shipping_obj = ShippingMethod.objects.filter(default=True)
        #default_shipping = {}
        if shipping_obj.count() > 0:
            default_shipping = shipping_obj[0]
        #Get cart sub total
        cart_id = request.session.get('cart_id')
        total_subtotal_obj = calculate_cart(cart_id)
        sub_total = total_subtotal_obj.get('sub_total')
        shipping_methods = []
        if float(sub_total) >= float('1000') and delivery_charge != True:
            cart_dict = calculate_cart(cart_id, default_shipping=default_shipping)
            shipping_methods.append(default_shipping)
        else:
            default_shipping = ShippingMethod.objects.get(pk=2)
            cart_dict = calculate_cart(cart_id, default_shipping=default_shipping)
            shipping_methods.append(default_shipping)
        response = {}
        html = ''
        i=1
        for shipping in shipping_methods:
            html += '<div class="form-group"><input type="radio" name="shipping_method" tabindex="1" id="shipping_method_'+str(i)+'" class="control shipping_method" value="'+str(shipping.id)+'" checked="checked"> <label for="shipping_method_'+str(i)+'" style="display: inline; cursor: pointer;"> '+str(shipping.name)+'- Rs. '+str(shipping.charge)+'</label></div>'
            i+=1 

        response['html'] = html
        response['shipping'] = cart_dict
        response['message'] = 'Success'
        return JsonResponse(response)
        
    return JsonResponse({"error": "Http Method not Allowed"})


def calculate_cart(cart_id, *args, **kwargs):
    #print('cart_id', cart_id)
    #print('args: ', args)
    #print('kwargs', kwargs)

    cart_obj = Cart.objects.get(pk=cart_id)
    cart_items = cart_obj.cartitem_set.all()
    total = 0
    subtotal = 0
    for item in cart_items:
        subtotal += float(item.product.actual_price) * item.quantity
    
    #If default shipping comes
    total = subtotal

    #print("Coupon: ", cart_obj.coupon)
    total = calculate_coupon(cart_obj, total)

    if kwargs.get('default_shipping'):
        charge = kwargs['default_shipping'].charge
        total = float(total)  + float(charge)
    

    if kwargs.get('payment_method'):
        method_charge = kwargs.get('payment_method').charge
        total = float(total) + float(method_charge)

    #print(total)

    context = {
        'sub_total': subtotal,
        'total': total
    }

    return context



def calculate_coupon(cart_obj, total):
    coupon_obj = cart_obj.coupon
    
    if coupon_obj is not None:
        if coupon_obj.is_percent:
            percent = coupon_obj.amount
            amount = ( total * percent ) / 100
        else:
            amount = coupon_obj.amount
    
        total = float(total) - float(amount)


    return total





def new_order_id():
    latest_order = Order.objects.order_by('-created_at').first()
    order_id = 100
    if latest_order:
        last_order_id = latest_order.order_id
        order_id = int(last_order_id) + 1

    return order_id


def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code', '')
    cart_id = request.session.get('cart_id')
    # If cart is none redirect to cart page
    if cart_id is None:
        messages.error(request, 'Cart is empty')
        return HttpResponseRedirect(reverse('ecommerce:cart'))

    if coupon_code != '':
        couponObj = Coupon.objects.filter(code=coupon_code).first()
        if couponObj is not None:
            # If coupon expiry is there, validate it
            if not couponObj.is_forever:
                expiry_date = couponObj.expiry
                current_date = date.today()
                #print('expiry_date: ',expiry_date, 'current_date: ', current_date)
                if current_date >= expiry_date:
                    messages.error(request, 'Coupon code has expired.')
                    return HttpResponseRedirect(reverse('ecommerce:cart'))


            cartObj = Cart.objects.get(pk=cart_id)
            cartObj.coupon = couponObj
            cartObj.save()
            messages.success(request, 'Coupon code applied successfully!')
        else:
            messages.error(request, 'Coupon code is invalide')

    # Redirect to cart page
    return HttpResponseRedirect(reverse('ecommerce:cart'))        


def remove_coupon(request):
    coupon_id = request.POST.get('coupon_id', None)
    if coupon_id:
        cart_id = request.session.get('cart_id')
        cart_obj = Cart.objects.get(pk=cart_id)
        cart_obj.coupon = None
        cart_obj.save()
        messages.success(request, 'Coupon removed successfully!')
    
    return HttpResponseRedirect(reverse('ecommerce:cart'))



def place_order(request):
    #print(request.POST)
    cart_data = request.POST
    cart_id = request.session.get('cart_id')
    if cart_id is not None:
        order_id = new_order_id()
        #print( order_id )
        userObj = {}
        cartObj = Cart.objects.get(pk=cart_id)
        if cartObj:
            userObj = cartObj.user

        shipping_id = cart_data['shipping_method']
        payment_id = cart_data['payment_method']
        
        name = cart_data['name']
        email = cart_data['email']
        mobile = cart_data['mobile']
        address = cart_data['address']
        postcode = cart_data['postcode']
        city = cart_data['city']
        state = cart_data['state']
        country = cart_data['country']
        
        shippingObj = {}
        shippingObj = ShippingMethod.objects.get(pk=shipping_id)
        paymentObj = PaymentMethod.objects.get(pk=payment_id)
        cart_dict = calculate_cart(cart_id, default_shipping=shippingObj, payment_method=paymentObj)

        # if shipping is same as billing 
        if cart_data.get('same_as_billing') and int(cart_data.get('same_as_billing')) == 1:
            shipping_name = name
            shipping_email = email
            shipping_mobile = mobile
            shipping_address = address
            shipping_postcode = postcode
            shipping_city = city
            shipping_state = state
            shipping_country = country
        else:
            shipping_name = cart_data['shipping_name']
            shipping_email = cart_data['shipping_email']
            shipping_mobile = cart_data['shipping_mobile']
            shipping_address = cart_data['shipping_address']
            shipping_postcode = cart_data['shipping_postcode']
            shipping_city = cart_data['shipping_city']
            shipping_state = cart_data['shipping_state']
            shipping_country = cart_data['shipping_country']


        #Check assure quantity is available
        qty_result = check_order_quantity(cartObj)
        if qty_result['allow'] == False:
            messages.error(request, "Insufficient quantity found!")
            return HttpResponseRedirect(reverse('ecommerce:cart'))

        #Get order by cart
        orderObj = get_order_by_cart(cartObj)
        #delete order if already exist with current cart
        #delete_order_by_cart(cartObj)

        if orderObj:
            orderObj.user = userObj
            orderObj.shipping_method = shippingObj
            orderObj.payment_method = paymentObj
            orderObj.subtotal = cart_dict['sub_total']
            orderObj.total = cart_dict['total']
            orderObj.billing_name = name
            orderObj.billing_email = email
            orderObj.billing_mobile = mobile
            orderObj.billing_address = address
            orderObj.billing_postcode = postcode
            orderObj.billing_mobile = mobile
            orderObj.billing_city = city
            orderObj.billing_state = state
            orderObj.billing_country = country
            orderObj.shipping_name = shipping_name
            orderObj.shipping_email = shipping_email
            orderObj.shipping_mobile = shipping_mobile
            orderObj.shipping_address = shipping_address
            orderObj.shipping_postcode = shipping_postcode
            orderObj.shipping_city = shipping_city
            orderObj.shipping_state = shipping_state
            orderObj.shipping_country = shipping_country
            orderObj.save()
        else: 
            # Prepare object to create order
            orderObj = Order.objects.create(
                order_id = order_id,
                cart = cartObj,
                user = userObj,
                shipping_method = shippingObj,
                payment_method = paymentObj,
                subtotal = cart_dict['sub_total'],
                total = cart_dict['total'],            
                billing_name = name,
                billing_email = email,
                billing_mobile = mobile,
                billing_address = address,
                billing_postcode = postcode,
                billing_city = city,
                billing_state = state,
                billing_country = country,
                shipping_name = shipping_name,
                shipping_email = shipping_email,
                shipping_mobile = shipping_mobile,
                shipping_address = shipping_address,
                shipping_postcode = shipping_postcode,
                shipping_city = shipping_city,
                shipping_state = shipping_state,
                shipping_country = shipping_country
            )

        #print("orderObj: ", orderObj)
        if orderObj:
            #Update cart
            cartObj.is_ordered = True
            cartObj.save()
            #If Payment method is Credit Card
            if int(payment_id) == 2:
                params = {}
                params['payment_id'] = payment_id
                params['order_id'] = orderObj.order_id
                #capture_payment(request, params)
                return HttpResponseRedirect(reverse('ecommerce:payment', kwargs={'order_id':orderObj.order_id}))

            else:
                # Delete cart and redirect to thank you page
                del request.session['cart_id']

                #Decrease product quantity
                decrease_order_quantity(cartObj)

                #Send order email
                send_order_email(orderObj)

                messages.success(request, 'Thank you for shopping with us.')
                #return HttpResponseRedirect(reverse('ecommerce:thankyou')+'?order_id='+orderObj.id)
                url = "%s?order_id=%s" % (reverse('ecommerce:thankyou'), orderObj.order_id)
                return HttpResponseRedirect(url)

        else:
            messages.error(request, 'Something went wrong while placing the order.')
            return HttpResponseRedirect(reverse('ecommerce:cart'))

    else:
        #messages.add_message(request, messages.INFO, 'Request Submitted Successfully!')
        messages.error(request, 'Your cart is empty, please try again.')
        return HttpResponseRedirect(reverse('ecommerce:cart'))

    #return HttpResponse('Place Order')



def send_order_email(order):
    #Order email for customer
    data = {}
    data['order'] = order
    data['toEmails'] = [order.billing_email]
    data['subject'] = 'Order Details: Medsbuy'
    send_email(data, 'order.html')

    #Order email for admin
    admin_email = get_emails('admin')
    data = {}
    data['order'] = order
    data['toEmails'] = [admin_email]
    data['subject'] = 'New Order: Medsbuy'
    send_email(data, 'order_admin.html')

    
def delete_order_by_cart(cart_obj):
    Order.objects.filter(cart=cart_obj).delete()

def get_order_by_cart(cart_obj):
    try:
        return Order.objects.get(cart=cart_obj)
    except Order.DoesNotExist:
        return None

def payment(request, order_id):
    #Get order details
    try:
        order_obj = Order.objects.get(order_id=order_id)
        order_cart_id = order_obj.cart.id
        cart_id = request.session.get('cart_id')
        if order_cart_id != cart_id:
            return HttpResponse("It is a wrong order id.")

        #client = razorpay.Client(auth=("rzp_test_mXbu1KlRESr23L", "6Xq6RBY7NwjQFgvmGPgxIxLW"))
        #client = razorpay.Client(auth=("rzp_test_34vmdEMr7sYilf", "oqAcZFXLaXRKOLDt9xcD3Vha"))
        client = razorpay.Client(auth=("rzp_live_nMhHRc4kqi5wVQ", "wlHe5A88SonfZACkk2lRB81u"))
        order_amount = int(order_obj.total) * 100
        order_currency = 'INR'
        #order_receipt = 'order_rcptid_11'
        #notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL
        payment_obj = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture='1'))
        order_id = order_id
        context = {
            'title':'Payment',
            'payment_obj':payment_obj,
            'order_id': order_id
        }
        return render(request, "carts/payment.html", context)
    except Order.DoesNotExist:
        return HttpResponse("Something went Wrong! Order Does Not Exist.")


def payment_success(request):
    if request.method == 'POST':
        #print("Posted in payment succes method2", request.POST)
        
        order_id = request.POST.get('order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        #Save payment info
        paymentObj = Payment.objects.create(order_id=order_id, razorpay_payment_id=razorpay_payment_id, razorpay_order_id=razorpay_order_id, razorpay_signature=razorpay_signature)

        cartObj = Cart.objects.get(pk=request.session.get('cart_id'))
        #Update order status
        orderObj = Order.objects.get(order_id=order_id)
        orderObj.status = 'success'
        orderObj.save()
        
        # Delete cart and redirect to thank you page
        del request.session['cart_id']

        #Decrease product quantity
        decrease_order_quantity(cartObj)

        #Send order email
        send_order_email(orderObj)

        messages.success(request, 'Thank you for shopping with us.')
        #return HttpResponseRedirect(reverse('ecommerce:thankyou')+'?order_id='+orderObj.id)
        url = "%s?order_id=%s" % (reverse('ecommerce:thankyou'), orderObj.order_id)
        return HttpResponseRedirect(url)


    context = {
        'title':'Payment Success'
    }
    return render(request, "carts/payment_success.html", context)
    