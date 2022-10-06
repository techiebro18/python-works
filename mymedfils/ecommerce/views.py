from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from products.models import Category, Brand, Product, get_products_by_category
from .forms import SignUpForm, LoginForm, MyaccountForm, ContactUsForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q,F, FloatField
from django.db.models.functions import Cast
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import ContactUs, Page, Slider, Subscribe, Zipcode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from mymedfils.helpers import encode_str, decode_str
from django.http import JsonResponse
from django.db import Error
from django.core import serializers
from django.core.cache import cache

def handler404(request, *args, **argv):
    context = {}
    return render(request, "ecommerce/404.html", context)


# Create your views here.
def welcome(request):
    #deals
    deals_prods = get_products_by_category('deals', limit=10)
    #hot-selling
    hot_selling_prods = get_products_by_category('hot-selling', limit=10)
    #homeopathy
    homeopathy_prods = get_products_by_category('homeopathy', limit=10)
    #ayurveda
    ayurveda_prods = get_products_by_category('ayurveda', limit=10)
    #unani
    unani_prods = get_products_by_category('unani', limit=10)
    #health-wellness
    health_wellness_prods = get_products_by_category('health-wellness', limit=10)
    #Top categories
    categories = top_categories()
    #Top brands
    brands = top_brands()
    #Sliders
    slides = Slider.objects.filter(id__in=[1,2,3,4,5,6], status=True)
    #Banners
    banners = Slider.objects.filter(id__in=[7,8,9], status=True)
    #Left Banners
    left_banners = Slider.objects.filter(id__in=[10,11,12], status=True)

    context = {
        'title': 'Medsbuy - Buy Online Medicine india | Free doctor consultation',
        'description': 'Get online genuine medicine at best price in India. Free home delivery and Cash on delivery (COD) is available. Free ayurvedic homeopathy and unani online doctor consultation.',
        'keyword': 'Online medicine in india, Online pharmacy in india, online medical store in india, Free unani consultation, Free Ayurvedic consultation, online medicine shop, best medicine store in india, best online pharmacy, pharmacy, medical store, online healthcare product in india ',
        'slides': slides,
        'banners': banners,
        'left_banners': left_banners,
        'categories': categories,
        'brands': brands,
        'deals_prods': deals_prods,
        'homeopathy_prods': homeopathy_prods,
        'ayurveda_prods': ayurveda_prods,
        'unani_prods': unani_prods,
        'health_wellness_prods': health_wellness_prods,
        'hot_selling_prods': hot_selling_prods
    }
    return render(request, "ecommerce/index.html", context)


def products_by_category(request, slug):
    cat_obj = Category.objects.get(slug=slug)
    sortby = request.GET.get('sortby', 'name')
    price = request.GET.get('price', None)
    brands = request.GET.get('brands[]', None)
    
    if price is not None or brands is not None:
        products = cat_obj.product_set.all()
        if brands is not None:
            brand_ids = request.GET.getlist('brands[]')
            #products = cat_obj.product_set.filter(brand__id__in(brand_ids))
            products = products.filter(brand__id__in=brand_ids)
        
        if price == 'below200':
           products = products.filter(price__lt=200)
        elif price == '200-500': 
           products = products.filter(price__range=(200, 500))
        elif price == '500-1000': 
           products = products.filter(price__range=(500, 1000))
        elif price == 'above1000': 
           products = products.filter(price__gt=1000)

    else:
        products = cat_obj.product_set.all()


    if sortby != '' and len(products) > 0:
        if sortby == 'popularity':
            pass
        elif sortby == 'price_asc':    
            products = products.order_by('price')
        elif sortby == 'price_desc':
            products = products.order_by('-price')
        elif sortby == 'discount':
            products = products.annotate(saleprice=Cast('sale_price', FloatField())).annotate(discount2=((F('price')-F('saleprice'))/F('price'))*100 ).order_by('-discount2')
        elif sortby == 'date':    
            products = products.order_by('-created_at')
        elif sortby == 'name':    
            products = products.order_by('name')

    #print(products)

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 52)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    #print(request.GET.getlist('brands[]'))
    context = {
        'title': 'Medsbuy | {}'.format(cat_obj.name),
        'category': cat_obj,
        'products': products
    }
    return render(request, 'products/products.html', context)



def products_by_brand(request, slug):
    brand_obj = Brand.objects.get(slug=slug)
    sortby = request.GET.get('sortby', 'name')
    price = request.GET.get('price', None)
    brands = request.GET.get('brands[]', None)
    
    if price is not None or brands is not None:
        products = brand_obj.product_set.all()
        if brands is not None:
            brand_ids = request.GET.getlist('brands[]')
            #products = cat_obj.product_set.filter(brand__id__in(brand_ids))
            products = products.filter(brand__id__in=brand_ids)
        
        if price == 'below200':
           products = products.filter(price__lt=200)
        elif price == '200-500': 
           products = products.filter(price__range=(200, 500))
        elif price == '500-1000': 
           products = products.filter(price__range=(500, 1000))
        elif price == 'above1000': 
           products = products.filter(price__gt=1000)

    else:
        products = brand_obj.product_set.all()


    if sortby != '' and len(products) > 0:
        if sortby == 'popularity':
            pass
        elif sortby == 'price_asc':    
            products = products.order_by('price')
        elif sortby == 'price_desc':
            products = products.order_by('-price')
        elif sortby == 'discount':
            products = products.annotate(saleprice=Cast('sale_price', FloatField())).annotate(discount2=((F('price')-F('saleprice'))/F('price'))*100 ).order_by('-discount2')
        elif sortby == 'date':    
            products = products.order_by('-created_at')
        elif sortby == 'name':    
            products = products.order_by('name')

    #print(products)

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 52)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    #print(request.GET.getlist('brands[]'))
    
    context = {
        'title': 'Medsbuy | {}'.format(brand_obj.name),
        'brand': brand_obj,
        'products': products
    }
    return render(request, 'products/brands-products.html', context)



def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    images  = product.productimage_set.all()
    simmilar_products = None
    categories_id = product.category.all().values_list('id', flat=True)
    categories_id_list = list(categories_id)
    #print(categories_id_list)
    if categories_id_list:
        simmilar_products = Product.objects.filter(category__in=categories_id_list).distinct()[0:30]

    context = {
        'title': 'Medsbuy | {}'.format(product.name),
        'product': product,
        'product_images': images,
        'simmilar_products': simmilar_products
    }
    return render(request, 'products/product_details.html', context)


def thankyou(request):
    context = {
        'title': 'Medsbuy | Thank You'
    }
    return render(request, 'ecommerce/thankyou.html', context)



def user_registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            #print("username: ", username)
            email = form.cleaned_data.get('email')
            #raw_password = form.cleaned_data.get('password1')
            raw_password = request.POST.get('pass1')
            # Create new user
            user_obj = User.objects.create_user(username, email=email, password=raw_password)
            user_obj.is_active = True
            #user_obj.set_password(raw_password)
            user_obj.save()

            #print(user_obj)
            # Save mobile in user profile
            '''mobile = form.cleaned_data.get('mobile')
            user_obj.profile.billing_mobile = mobile
            user_obj.profile.save()'''

            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            messages.success(request, 'You have been registered successfully!')
            return HttpResponseRedirect(reverse('ecommerce:user_registration'))
        else:
            """ messages.error(request, 'Please fill the form carefully!')
            return HttpResponseRedirect(reverse('ecommerce:user_registration')) """
            context = {
                'form': form
            }
            return render(request, 'ecommerce/signup.html', context)
    else:
        form = SignUpForm()
        context = {
            'title': 'Medsbuy | SignUp',
            'form': form
        }
        return render(request, 'ecommerce/signup.html', context)


def signin_form(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        username = ''
        if '@' in email:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                user_obj = None
            
            if user_obj is not None:
                username = user_obj.username
        else:
            username = request.POST.get('username', '')

        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        #print(user)
        if user is not None:
            login(request, user)
            #info, success, warning, error
            messages.success(request, 'You have logged in successfully!')
            return HttpResponseRedirect(reverse('ecommerce:myaccount_form'))
        else:
            messages.error(request, 'Credentials are not correct')
            return HttpResponseRedirect(reverse('ecommerce:signin_form'))

    else:    
        login_form = LoginForm()
        context = {
            'title': 'Medsbuy | SignIn',
            'form': login_form
        }
        return render(request, "ecommerce/signin.html", context)
    

#Send a password reset email
def forgot_password(request):
    context = {
            'title': 'Medsbuy | Forgot Password'
        }
    if request.method == "POST":
        email = request.POST.get('email', '')
        context['email'] = email
        if email != '':
            try:
                userObj = User.objects.get(email=email)
            except User.DoesNotExist:
                userObj = None
            
            if userObj is None:
                messages.error(request, "No user found with this email!")
                return render(request, "ecommerce/forgot-password.html", context)     
            
            # Prepare email for this user and send password reset link
            data = request.POST.copy()
            data['toEmails'] = [email]
            data['subject'] = 'Forgot Password: Medsbuy'
            encoded_email = encode_str(email)
            
            #data['reset_url'] = reverse('ecommerse:reset_password', kwargs={'email':encoded_email})
            data['reset_url'] = request.build_absolute_uri(reverse('ecommerce:reset_password', kwargs={'email':encoded_email}))
            send_email(data, 'forgot-password.html') 

            messages.success(request, "A password reset link has been sent to your email.")            
            return HttpResponseRedirect(reverse('ecommerce:forgot_password'))
            
        else:
            messages.error(request, "Please Enter Your Email")
            return HttpResponseRedirect(reverse('ecommerce:forgot_password'))
    else:
        return render(request, "ecommerce/forgot-password.html", context)


#Password reset page
def reset_password(request, email):
    context = {
            'title': 'Medsbuy | Reset Password'
        }
    if request.method == "POST":
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        try:
            decoded_email = decode_str(email)
            userObj = User.objects.get(email=decoded_email)
        except User.DoesNotExist:
            userObj = None

        if userObj is None:
            messages.error(request, "No user found with this email!")
            return HttpResponseRedirect(reverse('ecommerce:reset_password', kwargs={'email':email}))
            
        userObj.set_password(password1)
        userObj.save()

        messages.success(request, "Your password has been reset successfully!")
        return HttpResponseRedirect(reverse('ecommerce:reset_password', kwargs={'email':email}))

    else:
        context['email'] = email
        return render(request, "ecommerce/reset-password.html", context)
        



@login_required(login_url='/signin/')
def myaccount_form(request):
    current_user = request.user
    if request.method == 'POST':
        myaccount = MyaccountForm(request.POST)
        if myaccount.is_valid():
            current_user.username = myaccount.cleaned_data.get('username')
            current_user.first_name = myaccount.cleaned_data.get('first_name')
            current_user.last_name = myaccount.cleaned_data.get('last_name')
            current_user.email = myaccount.cleaned_data.get('email')
            current_user.save()
            
            current_user.profile.billing_mobile = myaccount.cleaned_data.get('mobile')
            current_user.profile.save()

            messages.success(request, 'Information updated successfully!')
            return HttpResponseRedirect(reverse('ecommerce:myaccount_form'))
        else:
            context = {
                'title': 'Medsbuy | My Account',
                'current_user':current_user,
                'form': myaccount
            }
            return render(request, "ecommerce/myaccount.html", context)
    else:
        #Auto populate form fields
        myaccount_dict = {'username':current_user.username, 'first_name':current_user.first_name, 'last_name':current_user.last_name, 'email':current_user.email, 'mobile':current_user.profile.billing_mobile} 
        context = {
            'title': 'Medsbuy | My Account',
            'current_user':current_user,
            'form': MyaccountForm(initial=myaccount_dict)
        }
        return render(request, "ecommerce/myaccount.html", context)


@login_required(login_url='/signin/')
def my_address(request):
    current_user = request.user

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        current_user.profile.billing_name = name
        current_user.profile.billing_email = email
        current_user.profile.billing_mobile = mobile
        current_user.profile.billing_address = address
        current_user.profile.billing_postcode = postcode
        current_user.profile.billing_city = city
        current_user.profile.billing_state = state
        current_user.profile.billing_country = country
        current_user.profile.save()

        messages.success(request, 'Address has been updated successfully!')
        return HttpResponseRedirect(reverse('ecommerce:my_address'))
    else:
        context = {
            'title': 'Medsbuy | My Address',
            'current_user':current_user
        }
        return render(request, "ecommerce/myaddress.html", context)


@login_required(login_url='/signin/')
def my_orders(request):
    current_user = request.user
    orders = current_user.order_set.all().order_by('-created_at')
    context = {
        'title': 'Medsbuy | My Orders',
        'orders': orders,
        'current_user': current_user
    }
    return render(request, "ecommerce/myorders.html", context)


@login_required(login_url='/signin/')
def order_details(request, order_id):
    current_user = request.user
    if request.method == "POST":
        order = Order.objects.get(order_id=order_id)
        order.status = 'canceled'
        order.save()
        messages.success(request, "Order status has been updated!")
        return HttpResponseRedirect(reverse('ecommerce:my_orders'))
    else:
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            order = None
        
        context = {
            'title': 'Medsbuy | Order Details',
            'order': order,
            'current_user':current_user
        }
        return render(request, "ecommerce/order_details.html", context)



@login_required(login_url='/signin/')
def change_password(request):
    current_user = request.user
    if request.method == "POST":
        #current_user.password = request.POST.get('password1')
        password = request.POST.get('password1')
        current_user.set_password(password)
        current_user.save()
        messages.success(request, "Password has been updated!")
        from_url = request.POST.get('from', '')
        if from_url == 'consultation':
            return HttpResponseRedirect(reverse('consultation:login'))
        else:
            return HttpResponseRedirect(reverse('ecommerce:signin_form'))
    else:
        context = {
            'title': 'Medsbuy | Change Password',
            'current_user':current_user
        }
        return render(request, "ecommerce/change_password.html", context)


def contact_us(request):

    if request.method == "POST":
        ContactUsFormObj = ContactUsForm(request.POST)
        if ContactUsFormObj.is_valid():
            ContactUsFormObj.save()
            messages.success(request, "Message has been sent successfully!")
            return HttpResponseRedirect(reverse('ecommerce:contact_us'))
        else:
            context = {
                'title': 'Medsbuy | Contact Us',
                'form': ContactUsFormObj
            }
            return render(request, "ecommerce/contact_us.html", context)        
    else:
        context = {
            'title': 'Medsbuy | Contact Us',
            'form': ContactUsForm()
        }
        return render(request, "ecommerce/contact_us.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return HttpResponseRedirect(reverse('ecommerce:home'))


def search(request):
    
    keyword = request.POST.get('keyword', '')
    if keyword == '':
        keyword = request.GET.get('keyword', '')
    cat_id = request.POST.get('cat_id', '')
    #Different ways of searching
    
    #Standard textual queries
    #products = Product.objects.filter(name__contains=keyword)
    
    #Case insensitive
    #products = Product.objects.filter(name__icontains=keyword)
    
    #PostgreSQL, Django provides specific tool to query
    #When dealing with English and Non English language
    #products = Product.objects.filter(name__unaccent__icontains=keyword)
    
    #a search for Helen will pick up Helena or Hélène, but not the reverse. Another option would be to use a trigram_similar comparison, which compares sequences of letters.
    #products = Product.objects.filter(name__unaccent__lower__trigram_similar=keyword)
    
    #Mulltiple conditions
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    #Filter on foreignkey property
    if cat_id != '':
        products = products.filter(category__id__in=[cat_id])

    #products = products.filter(~Q(category__id__in=[]))
    #products = products.filter(~Q(brand__id__in=[]))

    #cat_obj = Category.objects.get(slug=slug)
    sortby = request.GET.get('sortby', 'name')
    price = request.GET.get('price', None)
    brands = request.GET.get('brands[]', None)
    
    if price is not None or brands is not None:
        #products = cat_obj.product_set.all()
        if brands is not None:
            brand_ids = request.GET.getlist('brands[]')
            #products = cat_obj.product_set.filter(brand__id__in(brand_ids))
            products = products.filter(brand__id__in=brand_ids)
        
        if price == 'below200':
            products = products.filter(price__lt=200)
        elif price == '200-500': 
            products = products.filter(price__range=(200, 500))
        elif price == '500-1000': 
            products = products.filter(price__range=(500, 1000))
        elif price == 'above1000': 
            products = products.filter(price__gt=1000)

    else:
        #products = cat_obj.product_set.all()
        pass


    if sortby != '' and len(products) > 0:
        if sortby == 'popularity':
            pass
        elif sortby == 'price_asc':    
            products = products.order_by('price')
        elif sortby == 'price_desc':
            products = products.order_by('-price')
        elif sortby == 'discount':
            products = products.annotate(saleprice=Cast('sale_price', FloatField())).annotate(discount2=((F('price')-F('saleprice'))/F('price'))*100 ).order_by('-discount2')
        elif sortby == 'date':    
            products = products.order_by('-created_at')
        elif sortby == 'name':    
            products = products.order_by('name')

    if len(products) > 520:
        products = products[0:520]

    #print(products)
    all_products = products
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 52)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'title': 'Medsbuy | Search',
        'keyword': keyword,
        'products': products,
        'all_products': all_products
    }

    return render(request, "ecommerce/search.html", context)


def page(request, slug):
    title = None
    page = None
    try:
        page = Page.objects.get(slug=slug, status=True)
    except Page.DoesNotExist:
        if page is not None:
            title = page.name

    context = {
        'page': page,
        'title': title
    }
    return render(request, "ecommerce/page.html", context)


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


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        if email != '' and '@' in email:
            obj = Subscribe.objects.filter(email=email)
            print("obj:", obj)
            if not obj:
                subscribeObj = Subscribe.objects.create(email=email)
                messages.success(request, "You have been subscribed successfully!")
            else:
                messages.error(request, "You have already subscribed!")
        else:
                messages.error(request, "Please enter an email!")
    
    return HttpResponseRedirect(reverse('ecommerce:home'))



def custom_sitemap(request):
    context = {
        'title': 'Sitemap',
        'sitemaps': sitemaps
    }
    return render(request, "ecommerce/custom_sitemap.html", context)


def check_delivery_by_zipcode(request):
    #print(request.POST)
    data = {}
    data['code'] = 200
    try:
        if request.method == "POST":
            zipcode = request.POST.get('zipcode', '').strip()
            obj = Zipcode.objects.filter(zipcode=zipcode)
            if obj:
                data['obj'] = serializers.serialize("json", obj)
                data['message'] = "Success"
            else:
                data['message'] = "Zipcode not found!"
        else:
            data['message'] = "Method Not Allowed"
    except Error:
        data['code'] = 500
    
    return JsonResponse(data)



def get_city_by_zipcode(request):
    #print(request.POST)
    data = {}
    data['code'] = 200
    try:
        if request.method == "POST":
            zipcode = request.POST.get('zipcode', '').strip()
            obj = Zipcode.objects.get(zipcode=zipcode)
            tmp = {}
            tmp['zipcode'] = obj.zipcode
            tmp['city'] = obj.city.name
            tmp['state'] = obj.city.state.name
            tmp['country'] = obj.city.state.country.name
            data['obj'] = tmp
            data['message'] = "Success"
            
        else:
            data['message'] = "Method Not Allowed"
    except Zipcode.DoesNotExist:
        data['message'] = "Zipcode not found!"
    
    return JsonResponse(data)
    

def clear_cache(request):
    cache.clear()
    return HttpResponse('Cache Cleared!')


def top_categories():
    categories = Category.objects.order_by('-order')[:12]
    return categories


def top_brands():
    brands = Brand.objects.order_by('-order')[:12]
    return brands
