from django.urls import path, include 
from . import views

urlpatterns = [
    path('signup/', views.signup(), name="signup"),
    path("", views.login(), name="login"),
    path('menu/', views.menu_page(), name=("menu")),
    path('orders', views.order(), name="orders"),
]
