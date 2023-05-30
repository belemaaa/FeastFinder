from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, MenuItem, Order, OrderItem
from django.contrib import messages
import bcrypt
#from .utils import send_order_notification


# Create your views here.

#learn how to code well guy, your mates are making millions

def signup(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            phone = request.POST['phone']

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
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
                    password=hashed_password,
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
                request.session['customer'] = customer.name
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




# view to expand the details of an order
def order_details(request):
    order = get_object_or_404(Order)
    order_items = OrderItem.objects.filter(order=order)
    customer = order.customer

    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item')
        menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

        
        # Check if the menu item is already in the order items
        existing_order_item = order_items.filter(item=menu_item).first()


        if existing_order_item:
            # Increment the quantity and price if the item already exists
            existing_order_item.quantity += 1
            existing_order_item.price += menu_item.price 
            existing_order_item.save()

        else:
            # Create a new OrderItem and associate it with the Order
            order_item = OrderItem.objects.create(order=order, item=menu_item)
            order_items += order_item
        


        # Update the total price of the order
        order.total_price += menu_item.price  
        order.save()

        # Redirect back to the order detail page
        return redirect('order_details', order_id=order_id)   
    menu_items = MenuItem.objects.all()

    request.session['order_items'] = order_items
    request.session['order'] = order

    context = {
        'order': order,
        'order_items': order_items, 
        'customer': customer, 
        'menu_items': menu_items
    }
    return render(request, 'order_details.html', context)




# view to display order summary and checout the orders
def checkOut(request):
    order_items = request.session.get('order_items')
    order = request.session.get('order')
    customer = request.session.get('customer')

    context = {
        'order': 'order',
        'order_items': 'order_items',
        'customer': 'customer'

    }
    return render(request, "checkout.html", context)



    # items_ordered = request.session.get('items_ordered') or request.session.get('order_item')
    # total_price = request.session.get('total_price')

    # # Save the order in the database
    # order = Order(items_ordered=order, total_price=total_price)
    # order.save()

    #  # Notify admin about order
    # for item in order_details:
    #     print(f"New order received: {order.order_item}, Total price: {order.total_price}")

#hi



