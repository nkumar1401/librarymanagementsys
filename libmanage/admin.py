from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class Useradmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)

@admin.register(Author)
class Authoradmin(admin.ModelAdmin):
    list_display=('name','bio')
    search_fields = ('name',)

