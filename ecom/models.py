from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False, unique = True)
    date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *a, **k):
        self.slug = slugify(self.name)
        return super().save(*a, **k)


    @property
    def productypes(self):
        return self.product_types.all()

    class Meta:
        verbose_name_plural = 'Categories'

       
class ProductType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_types")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False, unique = True)

    @property
    def products(self):
        return self.products.all()

    def __str__(self):
        return f"{self.name}"

    def save(self, *a, **k):
        self.slug = slugify(self.name)
        return super().save(*a, **k)

       

class Product(models.Model):
    productype = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False, unique = True)
    file = models.ImageField(upload_to ="images/")
    price = models.FloatField()
    datetime = models.DateTimeField(auto_now_add= True, editable=False)
    

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *a, **k):
        self.slug = slugify(self.name)
        return super().save(*a, **k)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    paid = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add= True, editable=False)
    
    @property
    def cartprice(self):
        cartdetails = self.cartdetails.all()    
        total =0.0
        for detail in cartdetails:
            total += detail.totalprice
            
        return total

    
    @property
    def delivered(self):
        delivery = self.delivery    
        
        if not delivery or not delivery.delivered:
            return "No"
                  
        return "Yes"
    
    @property
    def noOfItems(self):
        return self.cartdetails.count()    
        
        

    

    def __str__(self):
        return f"{self.id}"

class Cartdetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartdetails")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartdetails")
    quantity = models.IntegerField()
    totalprice = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add= True, editable=False)
    

    def save(self, *a, **b):
        self.totalprice = self.product.price * self.quantity
        super().save()

#cryto, paystack
class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="payments")
    amount = models.FloatField(editable=False)
    total = models.FloatField(editable=False)
    reference = models.CharField(max_length=150)
    datetime = models.DateTimeField(auto_now_add= True, editable=False)
    
class Deliverypoint(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=18)
    email = models.EmailField()
    address = models.CharField(max_length= 200)
    cart = models.OneToOneField(Cart, unique=True, on_delete=models.CASCADE, related_name="delivery")
    delivered = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add= True, editable=False)
    