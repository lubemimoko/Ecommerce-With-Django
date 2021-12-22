from .models import *
from django.forms import ModelForm
    

class DeliveryForm( ModelForm):
    class Meta:
        model = Deliverypoint
        exclude = ["cart", "delivered"]

