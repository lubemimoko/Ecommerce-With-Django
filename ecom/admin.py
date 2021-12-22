from django.contrib import admin
from .models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "user", "datetime", "paid", "cartprice", "delivered", "noOfItems", "datetime")
    list_display = ("user", "noOfItems", "cartprice", "paid", "delivered", "datetime")

class CartdetailsAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "cart", "product", "quantity", "totalprice", "datetime")
    list_display = ("cart", "product", "quantity", "quantity", "totalprice", "datetime")

class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "cart", "total", "amount", "reference", "datetime")
    list_display = ("cart", "amount", "total", "reference", "datetime")

class DeliverypointAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "name", "email", "phone", "cart","address",  "datetime")
    list_display = ("name", "email", "phone", "cart","address", "delivered", "datetime")
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ( "name", "productype", "price", "file", "datetime")
    

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "slug" )
    

admin.site.register(Category)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Cartdetail, CartdetailsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Deliverypoint, DeliverypointAdmin)