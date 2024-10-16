from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookLoan, Author, Genre, Reservation
from rest_framework import generics, viewsets
from .serializers import UserRegistrationSerializer, AuthorSerializer, GenreSerializer, BookSerializer, ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return render(request, 'lib/book_list.html', {'books': serializer.data})

def loan_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        if book.stock_quantity > 0:
            BookLoan.objects.create(book=book, user=request.user)
            book.stock_quantity -= 1
            book.save()
            return redirect('loan_success')
    return render(request, 'lib/loan_book.html', {'book': book})

def loan_success(request):
    return render(request, 'lib/loan_success.html')

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ReservationView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        if book.stock_quantity > 0: 
            reservation = Reservation.objects.create(book=book, user=request.user)
            book.stock_quantity -= 1  
            book.save()
            return redirect('loan_success')

        return render(request, 'lib/reserve_failed.html', {'book': book})
class RootView(APIView):
    def get(self, request):
        return Response({
            "authors": request.build_absolute_uri('/authors/'),
            "genres": request.build_absolute_uri('/genres/'),
            "books": request.build_absolute_uri('/books/'),
            "register": request.build_absolute_uri('/register/')  # Add registration URL
        })