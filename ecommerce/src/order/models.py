from django.db import models
from django.db.models.signals import pre_save,post_save

from math import fsum

from cart.models import Cart

from ecommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
    )


# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=120,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99,max_digits=100,decimal_places=2)
    order_total = models.DecimalField(default=0,max_digits=100,decimal_places=2)
    
    def __str__(self):
        return self.order_id
    
    def update_total(self):
        print("update total")
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        payment_total = fsum([cart_total,shipping_total])
        formatted_payment_total = format(payment_total,'.2f')
        self.order_total = formatted_payment_total
        self.save()
        return payment_total
        

#generate order_id:random and unique
def pre_save_create_order_id(sender,instance,*args,**kwargs):
    print("generate id")
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id,sender=Order)

def post_save_cart_total(sender,instance,created,*args,**kwargs):
    print("save cart total")
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        print("cart total:")
        #card__id: 在order的cart里根据id进行lookup
        qs = Order.objects.filter(cart__id=cart_id)
        
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()
    
post_save.connect(post_save_order,sender=Order)     
        