from django.contrib import admin
from .models import *

admin.site.register(Book)
# admin.site.register(Author)
# class
admin.site.register(Genre)
admin.site.register(BookInstance)

