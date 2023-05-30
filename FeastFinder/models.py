from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=60, null=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    


class MenuItem(models.Model):
    image = models.ImageField(max_length=200, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}'
    


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #price = models.DecimalField(max_digits=100, decimal_places=2)
 
    def __str__(self):
        return f"Order #{self.id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

