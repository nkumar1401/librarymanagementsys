from rest_framework import permissions
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def book_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookReadserializer(books, many=True)
        return Response(serializer.data)
    
    if request.user.role != 'LIBRARIAN':
        return Response({"detail": "Only librarians can add books."}, status=status.HTTP_403_FORBIDDEN)

    serializer = BookWriteserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
