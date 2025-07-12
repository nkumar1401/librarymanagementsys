from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *
from .permission import IsLibrarian


class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = Authorserializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not IsLibrarian().has_permission(self.request, self):
            raise PermissionDenied('Only librarians can add authors.')
        serializer.save()


class GenreListCreateView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = Genreserializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not IsLibrarian().has_permission(self.request, self):
            raise PermissionDenied('Only librarians can add genres.')
        serializer.save()


class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        genre = request.GET.get('genre')
        author = request.GET.get('author')
        title = request.GET.get('title')

        if genre:
            books = books.filter(genres__name__icontains=genre)
        if author:
            books = books.filter(author__name__icontains=author)
        if title:
            books = books.filter(title__icontains=title)

        serializer = BookReadserializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsLibrarian().has_permission(request, self):
            raise PermissionDenied('Only librarians can add books.')
        serializer = BookWriteserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookReadserializer
        return BookWriteserializer

    def update(self, request, *args, **kwargs):
        if not IsLibrarian().has_permission(request, self):
            raise PermissionDenied('Only librarians can update books.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not IsLibrarian().has_permission(request, self):
            raise PermissionDenied('Only librarians can delete books.')
        return super().destroy(request, *args, **kwargs)


class BorrowListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'LIBRARIAN':
            borrows = BorrowRequest.objects.all()
        else:
            borrows = BorrowRequest.objects.filter(user=user)
        serializer = BorrowRequestserializer(borrows, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BorrowRequestserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BorrowApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != 'LIBRARIAN':
            raise PermissionDenied('Only librarians can approve requests.')

        borrow = get_object_or_404(BorrowRequest, pk=pk)
        if borrow.status != 'PENDING':
            return Response({'detail': 'Already processed.'}, status=400)

        borrow.status = 'APPROVED'
        borrow.approved_at = timezone.now()
        borrow.save()
        return Response({'status': 'approved'})


class BorrowRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != 'LIBRARIAN':
            raise PermissionDenied('Only librarians can reject requests.')

        borrow = get_object_or_404(BorrowRequest, pk=pk)
        if borrow.status != 'PENDING':
            return Response({'detail': 'Already processed.'}, status=400)

        borrow.status = 'REJECTED'
        borrow.save()
        return Response({'status': 'rejected'})


class BorrowReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        borrow = get_object_or_404(BorrowRequest, pk=pk)
        if borrow.status != 'APPROVED':
            return Response({'detail': 'Only approved books can be returned.'}, status=400)

        borrow.status = 'RETURNED'
        borrow.returned_at = timezone.now()
        borrow.save()
        return Response({'status': 'returned'})


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': Userserializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        data = request.data.copy()
        data['book'] = book_id
        serializer = BookReviewserializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListView(APIView):
    def get(self, request, id):
        reviews = BookReview.objects.filter(book_id=id)
        serializer = BookReviewserializer(reviews, many=True)
        return Response(serializer.data)
