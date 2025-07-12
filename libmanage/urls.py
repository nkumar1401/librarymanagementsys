from django.urls import path
from .views import *

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('genres/', GenreListCreateView.as_view(), name='genre-list-create'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('borrows/', BorrowListCreateView.as_view(), name='borrow-list-create'),
    path('borrows/<int:pk>/approve/', BorrowApproveView.as_view(), name='borrow-approve'),
    path('borrows/<int:pk>/reject/', BorrowRejectView.as_view(), name='borrow-reject'),
    path('borrows/<int:pk>/return/', BorrowReturnView.as_view(), name='borrow-return'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('books/<int:book_id>/reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('books/<int:id>/reviews/list/', ReviewListView.as_view(), name='review-list'),
]
