from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class Authorserializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



class Genreserializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookReadserializer(serializers.ModelSerializer):
    author = Authorserializer()
    genres = Genreserializer(many=True)

    class Meta:
        model = Book
        fields = '  __all__'


class BookWriteserializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__ '



class BorrowRequestserializer(serializers.ModelSerializer):
    book = BookReadserializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True, source='book')

    class Meta:
        model = BorrowRequest
        fields = ' __all__'
        read_only_fields = ['status', 'requested_at', 'approved_at', 'returned_at']



class BookReviewserializer(serializers.ModelSerializer):
    user = Userserializer(read_only=True)

    class Meta:
        model = BookReview
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
