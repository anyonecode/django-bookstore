from django.contrib import admin
from .models import Book, Order,MyProfile,Cart,favorite



admin.site.register(Book)
admin.site.register(Order)
admin.site.register(MyProfile)
admin.site.register(Cart)
admin.site.register(favorite)