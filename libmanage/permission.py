from .serializers import *
from rest_framework.generics import ListCreateAPIView 
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,BasePermission
from rest_framework import status



class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role=="LIBRARIAN")

class BookListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookReadserializer
        return BookWriteserializer

    def create(self, request, *args, **kwargs):
        if request.user.role != 'LIBRARIAN':
            return Response(
                {"detail": "Only librarians can add books."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)