from django.shortcuts import render,redirect
from django.utils.http import is_safe_url


from .forms import AddressForm

from billing.models import BillingProfile
from .models import Address

# Create your views here.
def checkout_address_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form":form
    }
    
    # where to go after user submit address
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    
    current_user = request.user
    
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        
        
        if current_user.is_authenticated:
            #login user checkout
            billing_profile,billing_profile_created = BillingProfile.objects.get_or_create(user=current_user,email=current_user.email)
        elif guest_email_id is not None:
            #guesr user checkout
            guest_email_object = GuestEmail.objects.get(id=guest_email_id)
            billing_profile,billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_object.email)
        else:
            pass
        
        if billing_profile is not None:
            address_type = request.POST.get('address_type','shipping')
            instance.billing_profile = billing_profile
            #get the address type from POST data, or use default type "shipping"
            instance.address_type = address_type
            instance.save()
            
            request.session[address_type+"_address_id"] = instance.id
            print(address_type+"_address_id")
            
        else:
            return redirect("/cart/checkout/")
            
        if is_safe_url(redirect_path,request.get_host()):
            print("redirect path:" + redirect_path)
            return redirect(redirect_path)
    return redirect("/cart/checkout/")

def checkout_address_reuse_view(request):
    
    # where to go after user select address
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    
    current_user = request.user
    
    if request.method == "POST":
        print(request.POST)
        shipping_address = request.POST.get('shipping_address',None)
        address_type = request.POST.get('address_type')
        if current_user.is_authenticated:
            billing_profile,billing_profile_created = BillingProfile.objects.get_or_create(user=current_user,email=current_user.email)
        else:
            pass
        
        if shipping_address is not None:
            qs = Address.objects.filter(billing_profile=billing_profile,id=shipping_address)
            if qs.exists():
                request.session[address_type+"_address_id"] = shipping_address
                print(address_type+"_address_id")
            if is_safe_url(redirect_path,request.get_host()):
                    print("redirect path:" + redirect_path)
                    return redirect(redirect_path)
    return redirect("/cart/checkout/")
