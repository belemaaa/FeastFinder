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

                return render(request, 'main/login.html')
            
        return render(request, 'main/signup.html')    


    except Exception as e:
        return render(request, 'main/404.html', {'error_message': str(e)})


def login(request):
        if request.method == 'POST':
            phone = request.POST['phone']

            customer = Customer.objects.get(phone=phone)
            
            if customer:
                request.session['customer'] = customer.phone
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


def order_item(request):
    
    pass


def order(request):
    customer = Customer.objects.get('phone')

    order_list = OrderItem.objects.all()





    cart_items = request.session.get('cart_items', {})
    menu_items = Menu.objects.filter(id__in=cart_items.keys())
    
    items = []
    total_price = 0.0
    for menu_item in menu_items:
        qty = cart_items[str(menu_item.id)]
        items.append({
            'menu_item': menu_item,
            'quantity': qty
        })
        total_price += menu_item.price * qty
    
    context = {
        'items': items,
        'total_price': total_price
    }
    
    return render(request, 'main/cart.html', context)
