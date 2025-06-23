from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


from .serializers import *
from .permission import *



@api_view(['GET', 'POST'])
def authorlistcreate(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = Authorserializer(authors, many=True)
        return Response(serializer.data)

    if request.user.role != 'LIBRARIAN':
        return Response({'detail': 'only librarian can add'}, status=status.HTTP_403_FORBIDDEN)

    serializer = Authorserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def genrelistcreate(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = Genreserializer(genres, many=True)
        return Response(serializer.data)

    if request.user.role != 'LIBRARIAN':
        return Response({'detail': 'only librarian can add genre'}, status=status.HTTP_403_FORBIDDEN)

    serializer = Genreserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
def booklistcreate(request):
    if request.method == 'GET':
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

    if request.user.role != 'LIBRARIAN':
        return Response({'detail': 'Only librarians can add books.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = BookWriteserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','DELETE'])
def bookdetail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method =='GET':
        serializer = BookReadserializer(book)
        return Response(serializer.data)
    
    if request.user.role != 'LIBRARIAN':
        return Response({'detail': 'only librarian can '}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = BookWriteserializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        book.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def borrowlistcreate(request):
    user = request.user

    if request.method == 'GET':
        if user.role == 'LIBRARIAN':
            borrows = BorrowRequest.objects.all()
        else:
            borrows = BorrowRequest.objects.filter(user=user)
        serializer = BorrowRequestserializer(borrows, many=True)
        return Response(serializer.data)

    serializer = BorrowRequestserializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def borrowapprove(request, pk):
    if request.user.role != 'LIBRARIAN':
        return Response({"detail": "Only librarians can approve requests."}, status=status.HTTP_403_FORBIDDEN)

    borrow = get_object_or_404(BorrowRequest, pk=pk)
    if borrow.status != 'PENDING':
        return Response({"detail": "Already processed."}, status=status.HTTP_400_BAD_REQUEST)

    borrow.status = 'APPROVED'
    borrow.approved_at = timezone.now()
    borrow.save()
    return Response({"status": "approved"})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def borrowreject(request, pk):
    if request.user.role != 'LIBRARIAN':
        return Response({"detail": "Only librarians can reject requests."}, status=status.HTTP_403_FORBIDDEN)

    borrow = get_object_or_404(BorrowRequest, pk=pk)
    if borrow.status != 'PENDING':
        return Response({"detail": "Already processed."}, status=  status.HTTP_400_BAD_REQUEST)

    borrow.status = 'REJECTED'
    borrow.save()
    return Response({"status": "rejected"})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def borrowreturn(request, pk):
    borrow = get_object_or_404(BorrowRequest, pk=pk)
    if borrow.status != 'APPROVED':
        return Response({"detail": "Only approved books can be returned."}, status=status.HTTP_400_BAD_REQUEST)

    borrow.status = 'RETURNED'
    borrow.returned_at = timezone.now()
    borrow.save()
    return Response({"status": "returned"})




@api_view(['POST'])
@permission_classes([AllowAny])
def registeruser(request):
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




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reviewcreate(request, book_id):
    data = request.data.copy()
    data['book'] = book_id
    serializer = BookReviewserializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def reviewlist(request,id):
    reviews = BookReview.objects.filter(book_id=id)
    serializer = BookReviewserializer(reviews, many=True)
    return Response(serializer.data)
