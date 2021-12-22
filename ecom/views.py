from django.shortcuts import render,redirect, get_object_or_404 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.db import transaction
from ecom.forms import DeliveryForm
from .models import *
from .utils import *
import json

# Create your views here.

categories = Category.objects.all()

def index(request):
    producttypes = ProductType.objects.all().order_by("-category")
    products = Product.objects.all().order_by("-id")

    data = {
        "producttypes":producttypes,
        "products":products,
        "categories":categories,
    }

    return render(request, "ecom/index.html", data)


def category(request, category):
    products = Product.objects.filter(category=category).order_by(id, -1)[:9]

    data = {
        "products":products,
        "categories":categories
    }


    return render(request, "ecom/index.html", data)

# @login_required
def cart(request):
    #if a user has an open cart, if yes then we will use the cart
    #cartid, productid, quantity
    if request.method == "POST":
        
        data = json.loads(request.body)
        
        try:
            cart = Cart.objects.get(user=request.user, paid=False)
        except:
            cart = Cart.objects.create(user=request.user)
        
        
        pid= data.get("product")
        quantity = data.get("quantity")
        
        # To check if the product exists in product Table
        try:
            product = Product.objects.get( id=pid)    
        except:
            return JsonResponse({"error":"Product does not exist"})
        
        #To update quantity if the product already exists
        if(Cartdetail.objects.filter(cart=cart, product=product).count() > 0):
                        
            total = product.price * float(quantity)
            c =  Cartdetail.objects.filter(cart=cart, product=product).update(quantity=quantity, totalprice=total )
        else:
            #To cart product in cart if it's not existing
            c =  Cartdetail.objects.create(cart=cart, product=product, quantity=quantity )
            
        myresponse = {"cart":cart.id, "product":product.id, "quantity":quantity}
        
        return JsonResponse({"success":myresponse})
    #then will add the items the user wants to buy into our cartdetails
    return JsonResponse({"error":"Invalid Request"})

# @login_required
def deleteitem(request):
    #a user can only delete an item if the cart is still open
    #a user can only delete he/she has created
    
    if request.method == "POST":
        
        data = json.loads(request.body)
        
        try:
            cart = Cart.objects.get(user=request.user, paid=False)
            pid= data.get("product")
            
            try:
                product = Product.objects.get( id=pid)    
            except:
                return JsonResponse({"error":"Product does not exist"})

            Cartdetail.objects.filter(cart = cart, product=product).delete()
            return JsonResponse({"success":"Deleted successfully"})
        except:
            return JsonResponse({"error": "Invalid Request"})
    return JsonResponse({"error": "Invalid Request"})    
    
def displaycart(request):
    cart = []
    if request.user:
        cart = Cart.objects.filter(user=request.user, paid=False).first()
    
    delivery = None
    if cart:
        delivery = Deliverypoint.objects.filter(cart=cart).values('email' ).first()
     
    data = {
        "cart":cart,
        "delivery":delivery,
    }

    return render(request, "ecom/cart.html", data)


def deliverypoint(request, id):
    delivery = Deliverypoint.objects.filter(cart=id).first()
    form = DeliveryForm(instance=delivery)

    if delivery and delivery.delivered == 1:
        pass
    else:
         if request.method== "POST":
            form = DeliveryForm( request.POST, instance=delivery)
            if form.is_valid():
                deliveryCommit = form.save(commit=False)
                deliveryCommit.cart_id = id
                deliveryCommit.save()
                
    data = {"form":form, "cart":id}
    return render(request, "ecom/deliverypoint.html", data)




def contact(request):
    
    return render(request, "ecom/contact.html")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("register")

    data = {
        "form":form
    }

    return render(request, "ecom/register.html", data)

def payment(request):
    
    data = json.loads(request.body)
    cartid = data.get("cartid")
    reference = data.get("reference")

    #to see if the payment with the reference number has already been recorded
    checkreference = Payment.objects.filter(reference=reference).exists()           

    # so if the reference number doesn't exists
    if not checkreference:
        resp = webhook(reference, cartid)

        #if cart is not found
        if resp.get("success") == -1:
            return JsonResponse({"message":resp.get("message")})

        #if cart is found then register payment
        amount = resp.get("amount")
        paystacktotal = resp.get("paystacktotal")
        cart = resp.get("cart")
        

        #Db Transaction
        with transaction.atomic():
            Payment.objects.create(cart=cart, reference=reference, amount=amount, total=paystacktotal)
                
            #setting message if amount is checked and found not to be complete
            message = {"message": "Payment was received, but the amount is not correct"}
                
            if amount >=2500:
                #import math module at the top
                total = math.ceil((amount+100)/(1-0.015))
            else: 
                total = math.ceil((amount)/(1-0.015))

            #if the amount coming from paystack and what we have calculated from the database are equal 
            if total == paystacktotal:
                #update cart(paid=True)
                Cart.objects.filter(id=cartid).update(paid=True)   
                message = {"message": resp.get("response") }
                return JsonResponse(message)
            else:
                return JsonResponse(message)            

    message = {"message": "Payment Has Been Recorded Already!"}
    return JsonResponse(message)
     
def history(request):
    cart = Cart.objects.filter(user=request.user)
    data = {"cart" : cart}
    return render(request, "ecom/history.html", data)


def sendmail(request):
    title = request.POST.get("title")
    message = request.POST.get("message")
    sender = request.POST.get("email")
    send_mail(title,message, sender, ['lubemimoko@gmail.com'], fail_silently=False)
    messages.success(request, "Mail Was Send Successfully")

    return redirect('contact')