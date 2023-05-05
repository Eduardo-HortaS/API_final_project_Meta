from django.db import models
from django.contrib.auth.models import User

### Superuser's username is superuser and it's password is 123
# auth_token --- 2a6a21cc71f63782828905673bbed8cf128fa47f 

### Manager's username is Mario and his password is pizzaMozar3554
# auth_token --- 6e4ea0797e833c73b2dc5e4f3968ea62e7587acf

### Delivery man's username is John and his password is justRock41
# auth_token --- d5b08c49729a981203c85e0b3652a53f8a122bc5

### Customer's username is Paul and his password is pastaMan70a
# auth_token --- 7818c848344cfb437fc1c408df3861a96f696ca4

### The user that we'll be setting to manager and later to delivery man:
# Adrian is his username and his password is Mozarella
# auth_token --- 2c5e65f61adfa081824c2025ec389de2d62ae1c6

## Tokens for each user in Djoser:

# 2c5e65f61adfa081824c2025ec389de2d62ae1c6	Adrian	May 1, 2023, 8:33 p.m.
# 7818c848344cfb437fc1c408df3861a96f696ca4	Paul	May 1, 2023, 1:45 a.m.
# d5b08c49729a981203c85e0b3652a53f8a122bc5	John	May 1, 2023, 1:45 a.m.
# 2a6a21cc71f63782828905673bbed8cf128fa47f	superuser	May 1, 2023, 1:45 a.m.
# 6e4ea0797e833c73b2dc5e4f3968ea62e7587acf	Mario	May 1, 2023, 12:41 a.m.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ( 'menuitem', 'user')
        
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True) # This part could prove to be wrong, if it is, you wouldn't want be able to access delivery crew members with it, check the /api/orders/{orderId} endpoint for updates by the manager!!!
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menuitem')