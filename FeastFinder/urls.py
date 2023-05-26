from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup(), name="signup"),
    path("", views.login(), name="login"),
    path('menu/', views.menu_page(), name=("menu")),
    path('order details/', views.order_details(), name="order_details"),
    path('checkout/', views.checkOut(), name="checkout")
]
