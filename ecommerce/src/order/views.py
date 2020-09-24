from django.shortcuts import render
from billing.models import BillingProfile

# Create your views here.
def history_orders_view(request):
    current_user = request.user
    billing_profile = None
    
    if current_user.is_authenticated:
        billing_profile,billing_profile_iscreated = BillingProfile.objects.get_or_create(user=current_user,email=current_user.email)
        
    if billing_profile is not None:
        order_qs = billing_profile.order_set.all()
        paid_order_qs = order_qs.filter(status="paid")
        
        
        if order_qs.exists():
            context = {"order_qs":paid_order_qs,"has_order":True}
            print("current user has orders")
            
        else:
            context = {"order_qs":paid_order_qs,"has_order":False}
            print("no orders")
        
    return render(request, "orders.html", context)
    