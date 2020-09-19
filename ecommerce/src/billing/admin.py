from django.contrib import admin

# Register your models here.
from .models import BillingProfile
from .models import Card
from .models import Charge

admin.site.register(BillingProfile)
admin.site.register(Card)
admin.site.register(Charge)