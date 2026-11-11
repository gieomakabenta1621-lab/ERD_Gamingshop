from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
 path("",views.home,name="home"),
 path("cart/",views.cart,name="cart"),
 path("cart/add/<int:product_id>/",views.add_to_cart,name="add_to_cart"),
 path("cart/update/<int:line_id>/",views.update_cart,name="update_cart"),
 path("checkout/",views.checkout,name="checkout"),
 path("orders/",views.orders,name="orders"),
 path("login/",auth_views.LoginView.as_view(template_name="store/login.html"),name="login"),
 path("logout/",auth_views.LogoutView.as_view(),name="logout"),
 path("register/",views.register,name="register"),
]
