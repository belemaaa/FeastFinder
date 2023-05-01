from django.shortcuts import render, redirect
from .models import Customer, Menu, Order, OrderItem

# Create your views here.

def signup(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            phone = request.POST['phone']

            existing_customer = Customer.objects.filter(phone=phone)

            if existing_customer:
                context = {
                   'error': 'User already exists'
                }
                return render(request, 'main/signup.html', context)
            
            else:
                new_customer = Customer(
                    name=name,
                    email=email,
                    passowrd=password,
                    phone=phone
                )
                new_customer.save()
                return render(request, 'main/login.html')
            
        return render(request, 'main/signup.html')    


    except Exception as e:
        return render(request, 'main/404.html', {'error_message': str(e)})
