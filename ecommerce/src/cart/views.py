from django.shortcuts import render,redirect
from django.contrib import messages


from products.models import Product
from .models import Cart

def cart_home(request):
    cart_obj,new_obj = Cart.objects.new_or_get_cart(request)
    products = cart_obj.products.all()
    total = 0
    for i in products:
        total += i.price
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
  
    #if product_obj in cart_obj.products.all():
     #   cart_obj.products.remove(product_obj)
    #else:
    if product_obj.stock >= 1:  
        cart_obj.products.add(product_obj)
        product_obj.sold += 1
        product_obj.stock = product_obj.quantity - product_obj.sold
        product_obj.save()
        return redirect('cart')
    else:
        messages.info(request,"The product is out of stock currently!")
        return redirect(request.META['HTTP_REFERER'])
    print(cart_obj.products.all())
    