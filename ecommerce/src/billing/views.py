from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url

import stripe
stripe.api_key = "sk_test_51HRwMeEcligTwCtGTBzUurE2xEXgFforhjIu7PKZp4fFFd5SH0jQeihxfWuRKwmR87GN615oWDINevLx3jDw80an00JgigGJag"
STRIPE_PUBLISHABLE_KEY = "pk_test_51HRwMeEcligTwCtGrB70qW1aPm94C4P6f8U3Mdo8CJ1mYFRJau5OH0zeFGq3CXmeGYZ7taXrRKTJwCQGcR5krfpL00jlRIytcR"

# Create your views here.
def payment_method_view(request):
    nextURL = None
    next_ = request.GET.get('next')
    
    if is_safe_url(next_ ,request.get_host()):
        nextURL = next_
    
    
    context = {"stripe_publishable_key":STRIPE_PUBLISHABLE_KEY,"nextURL":nextURL}
    if request.method == "POST":
        print(request.POST)
    return render(request, "paymentmethod.html", context)

def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax:
        print(request.POST)
        return JsonResponse({"message":"Card added"})
    return HttpResponse("error",status_code=401)