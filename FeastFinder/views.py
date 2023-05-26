from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Menu, MenuItem, Order, OrderItem


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
    menu_items = MenuItem.objects.all()

    context = {
        'menu_items': menu_items
    }
    return render(request, 'main/menu.html', context)  



# view to order menu items 
# behaves like an add to cart method
def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    customer = order.customer
    
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item')
        menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
        
        # Check if the menu item is already in the order items
        existing_order_item = order_items.filter(item=menu_item).first()

        if existing_order_item:
            # Increment the quantity if the item already exists
            existing_order_item.quantity += 1
            existing_order_item.save()

        else:
            # Create a new OrderItem and associate it with the Order
            order_item = OrderItem.objects.create(order=order, item=menu_item)
        

        # Redirect back to the order detail page
        return redirect('order', order_id=order_id)
    
    menu_items = MenuItem.objects.all()

    context = {
        'order': order,
        'order_items': order_items, 
        'customer': customer, 
        'menu_items': menu_items
    }
    return render(request, 'order.html', context)




# def order_item(request):

#     pass


# def order(request):
#     customer = Customer.objects.get('phone')

#     order_list = OrderItem.objects.all()





#     cart_items = request.session.get('cart_items', {})
#     menu_items = Menu.objects.filter(id__in=cart_items.keys())
    
#     items = []
#     total_price = 0.0
#     for menu_item in menu_items:
#         qty = cart_items[str(menu_item.id)]
#         items.append({
#             'menu_item': menu_item,
#             'quantity': qty
#         })
#         total_price += menu_item.price * qty
    
#     context = {
#         'items': items,
#         'total_price': total_price
#     }
    
#     return render(request, 'main/cart.html', context)
