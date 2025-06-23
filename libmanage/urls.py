
from django.urls import path
from .views import  *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('authors/', authorlistcreate, name='author-list-create'),
    path('genres/',genrelistcreate, name='genre-list-create'),
    path('books/',booklistcreate, name='book-list-create'),
    path('books/<int:pk>/', bookdetail, name='book-detail'),
    path('borrow/', borrowlistcreate, name='borrow-request-list-create'),
    path('borrow/<int:pk>/approve/', borrowapprove, name='borrow-approve'),
    path('borrow/<int:pk>/reject/', borrowreject, name='borrow-reject'),
    path('borrow/<int:pk>/return/', borrowreturn, name='borrow-return'),
    path('books/<int:book_id>/reviews/', reviewlist, name='review-list'),
    path('books/<int:book_id>/reviews/add/', reviewcreate, name='review-create'),
    path('register/', registeruser, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
