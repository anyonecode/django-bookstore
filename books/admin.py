from django.contrib import admin
from .models import Book, Order,MyProfile,Cart



admin.site.register(Book)
admin.site.register(Order)
admin.site.register(MyProfile)
admin.site.register(Cart)