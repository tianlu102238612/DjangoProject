from django.db import models


class ProductManager(models.Manager):
    def get_by_id(self,id):
        #self.get_queryset == Product.objects
        queryset = self.get_queryset().filter(id=id)    
        if queryset.count() == 1:
            return queryset.first()
        return None

# Create your models here.
class Product(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    image       = models.ImageField(upload_to='products/',null=True,blank=True)
    quantity    = models.IntegerField(default=0)
    sold        = models.IntegerField(default=0)
    stock       = models.IntegerField(default=0)
    
    objects = ProductManager()
    
    def __unicode__(self):
        return self.title
        
    def __str__(self):
        return self.title