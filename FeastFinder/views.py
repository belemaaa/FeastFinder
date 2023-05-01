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
                customer = Customer(
                    name=name,
                    email=email,
                    password=password,
                    phone=phone
                )
                customer.save()
                request.session['customer_id'] = customer.id

                return render(request, 'main/login.html')
            
        return render(request, 'main/signup.html')    


    except Exception as e:
        return render(request, 'main/404.html', {'error_message': str(e)})


def login(request):
        if request.method == 'POST':
            phone = request.POST['phone']

            customer = Customer.objects.get(phone=phone)
            
            if customer:
                request.session['customer'] = customer.id
                return redirect('home')
            
            else:
                context = {
                    'error': 'invalid login details'
                }
                return render(request, 'main/login.html', context)
            
        return render(request, 'main/login.html')


def menu_page(request):
    menu_items = Menu.objects.all()

    context = {
        'menu_items': menu_items
    }
    return render(request, 'main/menu.html', context)        