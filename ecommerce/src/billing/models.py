from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save


import stripe
stripe.api_key = "sk_test_51HRwMeEcligTwCtGTBzUurE2xEXgFforhjIu7PKZp4fFFd5SH0jQeihxfWuRKwmR87GN615oWDINevLx3jDw80an00JgigGJag"



User = settings.AUTH_USER_MODEL
# Create BillingProfile Model
class BillingProfile(models.Model):
    #one user can have only one billing profile
    #allow guest users to login: can be null or blank
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, blank=True,null=True)
    
    def __str__(self):
        return self.email

### create customer id    
def billing_profile_created_receiver(sender, instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        print("api request send to stripe")
        customer = stripe.Customer.create(
            email=instance.email
        )
        print(customer)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        #instance: AUTH_USER_MODEL
         BillingProfile.objects.get_or_create(user=instance,email=instance.email)
         
#def billing_profile_created_receiver(sender,instance,created,*args,**kwargs):
    
post_save.connect(user_created_receiver,sender=User)



    
    



















