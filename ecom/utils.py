import json
import math
from django.http.response import JsonResponse
from .models import *
import requests
def getcart(user):
    try:
        c = Cart.objects.get(user=user, paid=False)
        cart = Cartdetail.objects.filter(cart=c)
    except:
        cart = []
        
    return cart
    
def webhook(reference, cartid ):
    #secret_key,ref, 
    secret_key = "xxxxx"
    
    #endpoint for verification
    url = "https://api.paystack.co/transaction/verify/"+reference

    #headers that we will be sending
    headers = {
        "Authorization": "Bearer " + secret_key,
        "Cache-Control": "no-cache",
    }
    
    #make the api request to paystack
    response = requests.get(url, headers=headers)
    # response should be in JSON format
    response = response.json()
    
    #to check status
    if response["status"] == True:
        #to check the total amount needed to be paid for a cart
        
        try:
            cart = Cart.objects.get(id=cartid)
        except:
            return {"message":"Cart Not Found", "success":-1}

        amount = float(cart.cartprice)
        paystacktotal = float(response["data"]["amount"]/100)

        return {"response": response["message"], "amount":amount, "paystacktotal":paystacktotal, "cart":cart, "success":1}
    else:
        return {"success":-1, "message":"Payment Was Not Confirmed By Paystack"}    