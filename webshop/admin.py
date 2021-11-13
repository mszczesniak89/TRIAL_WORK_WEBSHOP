from django.contrib import admin

# Register your models here.
from django.contrib import admin
from webshop.models import Product, ShoppingCart, ShoppingCartItems, Category, Manufacturer
# Register your models here.
admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItems)
admin.site.register(Category)
admin.site.register(Manufacturer)
