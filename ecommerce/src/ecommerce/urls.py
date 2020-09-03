"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

from django.contrib import admin
from django.urls import path


from .views import home_page,logout_view
from accounts.views import login_page,register_page

from products.views import ProductListView,product_list_view,product_detail_view
from cart.views import cart_home,cart_update,checkout_home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home_page),
    path('login/',login_page,name="login"),
    path('logout/',logout_view,name="logout"),
    path('register/',register_page,name="register"),
    path('products/',product_list_view,name="products"),
    path('products/<int:pk>/',product_detail_view,name="products_detail"),
    path('search/',include("search.urls")),
    path('cart/',cart_home,name='cart'),
    path('cart/update/',cart_update,name='update'),
    path('cart/checkout/',checkout_home,name="checkout")
]

if settings.DEBUG:
   urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
   urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 