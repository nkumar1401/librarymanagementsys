from django.db import models
from django.contrib.auth.models import AbstractUser
from decouple import config
from django.contrib.auth import password_validation
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        LIBRARIAN = 'LIBRARIAN',  'Librarian'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    def __str__(self):
        return self.username



class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    ISBN = models.CharField(max_length=10, unique=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        RETURNED = 'RETURNED', 'Returned'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} - {self.book.title} ({self.status})'

from django.core.validators import MaxValueValidator ,MinValueValidator 

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.user.username}'

