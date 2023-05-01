from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60, null=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_digits=15)

    def __str__(self):
        return self.name
    

class Menu(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_length=20, decimal_places=2)
    image = models.ImageField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name} ({self.price})"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.customer
    
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item}"
    
    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
    

