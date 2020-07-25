from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.http import Http404

from .models import Product
from cart.models import Cart

class ProductListView(ListView):
    queryset = Product.objects.all()
    

def product_list_view(request):
    queryset = Product.objects.all()
    context = {'object_list':queryset}
    return render(request,"products/list.html",context)



    

def product_detail_view(request,pk):
    get_object = Product.objects.get_by_id(pk)
         #every object in django has a primary key,which is id
    if get_object is None:
        raise Http404("Product doesn't exist")
    
    context = {'object':get_object}
    
    
    return render(request,"products/detail.html",context)