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
@admin.register(BookReview)
class BookReviewadmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    search_fields = ('user__username', 'book__title')
    list_filter = ('rating',)    

@admin.register(Book)
class Bookadmin (admin.ModelAdmin):
    list_display = ('title', 'author', 'ISBN', 'total_copies', 'available_copies')
    search_fields = ('title', 'author__name', 'ISBN')
    list_filter = ('author', 'genres')

@admin.register(Genre)
class Genreadmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)