from django.db import models
from billing.models import BillingProfile

# Create your models here.

ADDRESS_TYPE = (
    ('billing','Billing Address'),
    ('shipping','Shipping Address'),
    )

class Address(models.Model):
    billing_profile  = models.ForeignKey(BillingProfile,on_delete=models.CASCADE )
    address_type     = models.CharField(choices=ADDRESS_TYPE,max_length=120)
    address_line_1   = models.CharField(max_length=120)
    address_line_2   = models.CharField(max_length=120,null=True,blank=True)
    city             = models.CharField(max_length=120)
    country          = models.CharField(max_length=120)
    state            = models.CharField(max_length=120)
    suburb           = models.CharField(max_length=120)
    postcode         = models.CharField(max_length=120)
    
    def __str__(self):
        return str(self.billing_profile)