from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem

# Define a list of models to register
models = [Category, MenuItem, Cart, Order, OrderItem]

# Register all models in the list using a loop
for model in models:
    admin.site.register(model)
    
