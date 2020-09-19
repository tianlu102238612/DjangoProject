from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.http import HttpResponse

#################################################################################################
import stripe
stripe.api_key = "sk_test_51HRwMeEcligTwCtGTBzUurE2xEXgFforhjIu7PKZp4fFFd5SH0jQeihxfWuRKwmR87GN615oWDINevLx3jDw80an00JgigGJag"

User = settings.AUTH_USER_MODEL
#################################################################################################

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
    
    def charge(self,order_obj,card=None):
        return Charge.objects.conductCharge(self,order_obj,card)


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
             
post_save.connect(user_created_receiver,sender=User)


#################################################################################################
class CardManager(models.Manager):
    new_card = None
    def add_new_card(self,billing_profile,stripe_card_response):
        new_card = self.model(billing_profile=billing_profile,
                              stripe_id = stripe_card_response.id,
                              brand = stripe_card_response.brand,
                              country = stripe_card_response.country,
                              fingerprint = stripe_card_response.fingerprint,
                              last4 = stripe_card_response.last4,
                              )
        new_card.save()
        print("new card saved")
        return new_card

class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True,null=True)
    country = models.CharField(max_length=120, blank=True,null=True)
    fingerprint = models.CharField(max_length=120, blank=True,null=True)
    last4 = models.CharField(max_length=120, blank=True,null=True)
    
    default = models.BooleanField(default=True) #set default card
    
    objects = CardManager()
    
    def __str__(self):
        return self.last4


#################################################################################################

class ChargeManager(models.Manager):
   
    def conductCharge(self,billing_profile,order_obj,card=None):   #Charge.objects.conductCharge()
        ### 第一步：先检查有没有可以用来支付的卡，没有指定的卡就看有没有默认的
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)#reverse relationship: 每个card都要associate一个billingprofile，所以也可以通过billing profile来查询卡
            if cards.exists():
                card_obj = cards.first()
        print("check if card is available: ")
        print(cards)
        
        if card_obj is None:
            return False, "You have not add any payment card"
        
        #### 第二步：创建一个charge，并在response里获得一系列返回值:https://stripe.com/docs/api/charges/create
        charge_create_response = stripe.Charge.create(
              amount = int(order_obj.order_total * 100),
              currency = "aud",
              customer = billing_profile.customer_id,  #The ID of an existing customer that will be charged in this request.
              source = card_obj.stripe_id,  #payment source to be charged, this can be the ID of a card,a token
              metadata = {"order_id":order_obj.order_id}
            )
        print("create a charge: ")
        print(charge_create_response)
        
        
        ### 第三步：基于charge_create_response这个回应里存储的信息，来实例化一个Card对象
        new_charge_obj = self.model(
            billing_profile = billing_profile,
            stripe_id = charge_create_response.id,
            paid = charge_create_response.paid,
            refunded = charge_create_response.refunded,
            outcome = charge_create_response.outcome,
            outcome_type = charge_create_response.outcome["type"],
            seller_message = charge_create_response.outcome["seller_message"],
            risk_level = charge_create_response.outcome["risk_level"],
            )
        
        new_charge_obj.save()
        
        return new_charge_obj.paid,new_charge_obj.outcome
        
        

class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)
    
    paid = models.BooleanField(default=False)  #true if the charge succeeded, or was successfully authorized for later capture.
    refunded = models.BooleanField(default=False) #A list of refunds that have been applied to the charge.
    
    outcome = models.TextField(blank=True,null=True) #Details about whether the payment was accepted, and why. 
    outcome_type = models.CharField(max_length=120,blank=True,null=True) #Possible values are authorized, manual_review, issuer_declined, blocked, and invalid
    seller_message = models.CharField(max_length=120,blank=True,null=True) #A human-readable description of the outcome type and reason
    risk_level = models.CharField(max_length=120,blank=True,null=True) #Possible values for evaluated payments are normal, elevated, highest
    
    
    objects = ChargeManager()



 













