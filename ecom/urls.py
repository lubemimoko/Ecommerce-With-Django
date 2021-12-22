from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView 

urlpatterns = [
   path("", views.index, name="home"),
   path("cart/", views.cart, name="cart"),
   path("deleteitem/", views.deleteitem, name="deleteitem"),
   path("display/cart/", views.displaycart, name="displaycart"),
   path("contact/", views.contact, name="contact"),
   path("checkout/<int:id>", views.deliverypoint, name="checkout"),
   path("payment/", views.payment, name="payment"),
   path("purchase/history/", views.history, name="history"),
   path("sendmail", views.sendmail, name="sendmail"),

   path("register/", views.register, name="register"),
   path("login/", LoginView.as_view(template_name = "ecom/login.html"), name="login"),
   path("logout/", LogoutView.as_view(), name="logout"),
   # path("test/", views.test, name="test")
]

#url/routes -> views(Logic) -> templates