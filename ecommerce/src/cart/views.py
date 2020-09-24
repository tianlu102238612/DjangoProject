from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponse

from products.models import Product
from .models import Cart
from order.models import Order
from accounts.models import GuestEmail
from billing.models import BillingProfile
from addresses.models import Address

from addresses.forms import AddressForm
from accounts.forms import LoginForm,RegisterForm,GuestForm

STRIPE_PUBLISHABLE_KEY = "pk_test_51HRwMeEcligTwCtGrB70qW1aPm94C4P6f8U3Mdo8CJ1mYFRJau5OH0zeFGq3CXmeGYZ7taXrRKTJwCQGcR5krfpL00jlRIytcR"

def cart_home(request):
    cart_obj,new_obj = Cart.objects.new_or_get_cart(request)
    products = cart_obj.products.all()
    total = 0
    
    for product in products:
        total += product.price
        
    print(total)
    cart_obj.total = total
    cart_obj.save()
    context = {"cart":cart_obj}
    
    
    return render(request,"cart/home.html",context)



def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    cart_obj,new_cart_obj = Cart.objects.new_or_get_cart(request)
  
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
        added = False
    else:
        if product_obj.stock >= 1:  
            cart_obj.products.add(product_obj)
            product_obj.sold += 1
            product_obj.stock = product_obj.quantity - product_obj.sold
            product_obj.save()
            added = True
            return redirect('cart')
        else:
            messages.info(request,"The product is out of stock currently!")
            return redirect(request.META['HTTP_REFERER'])
        
        if request.is_ajax:
            print("Ajax request")
            
            json_data = {
                "cart_id":cart_obj.id,
                "products":list(cart_obj.products.values()),
                "added":added,
                "removed":not added,
                }
            return JsonResponse(json_data)
    print(cart_obj.products.all())



def checkout_home(request):
    cart_obj,new_cart_created = Cart.objects.new_or_get_cart(request)
    order_obj = None
    if new_cart_created or cart_obj.products.count()==0:
        return redirect('/cart')
    else:
        order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj,active=True,status='created')
        
    current_user = request.user
    billing_profile = None
    login_form = LoginForm() 
    guest_form = GuestForm()
    address_form = AddressForm()
    user_is_auth = False
    
    guest_email_id = request.session.get('guest_email_id')
    billing_address_id = request.session.get('billing_address_id',None)
    shipping_address_id = request.session.get('shipping_address_id',None)
    
    
    
    if current_user.is_authenticated:
        #login user checkout
        user_is_auth = True
        billing_profile,billing_profile_created = BillingProfile.objects.get_or_create(user=current_user,email=current_user.email)
    elif guest_email_id is not None:
        #guesr user checkout
        guest_email_object = GuestEmail.objects.get(id=guest_email_id)
        billing_profile,billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_object.email)
    else:
        pass
    
    address_qs = None
    user_has_card = False
    default_card = None
    if billing_profile is not None:
        user_has_card = billing_profile.user_has_card
        default_card = billing_profile.default_card
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        #shipping_address = address_qs.filter(address_type = 'shipping' )
        #billing_address = address_qs.filter(address_type = 'billing' )
        order_qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
           # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            #if old_order_qs.exists():
            #    old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile = billing_profile, cart = cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
    
    if request.method == "POST":
        is_valid = order_obj.checkout_valid()
        if is_valid:
            is_paid, seller_msg = billing_profile.charge(order_obj)
            if is_paid:
                order_obj.change_status_to_paid()
                del request.session['cart_id']
                return HttpResponse("checkout success")
            else:
                return HttpResponse("checkout failed")
                print(seller_msg)


    context = {"order_object":order_obj,
               "billing_profile":billing_profile,
               "login_form":login_form,
               "guest_form":guest_form,
               'address_form':address_form,
               'address_qs':address_qs,
               'user_has_card':user_has_card,
               'STRIPE_PUBLISHABLE_KEY':STRIPE_PUBLISHABLE_KEY,
               'user_is_auth':user_is_auth,
               "default_card":default_card,
               }
    
    
    return render(request,"cart/checkout.html",context)

