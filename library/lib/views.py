from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookLoan, Author, Genre, Reservation
from rest_framework import generics, viewsets
from .serializers import UserRegistrationSerializer, AuthorSerializer, GenreSerializer, BookSerializer, ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

def is_staff(user):
    return user.is_staff

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return render(request, 'lib/book_list.html', {'books': serializer.data})

@login_required
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

    def get(self, request):
    
        return render(request, 'registration/register.html')  

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AuthorViewSet(LoginRequiredMixin, UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def test_func(self):
        return self.request.user.is_staff

class GenreViewSet(LoginRequiredMixin, UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def test_func(self):
        return self.request.user.is_staff

class BookViewSet(LoginRequiredMixin, UserPassesTestMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def test_func(self):
        return self.request.user.is_staff

class ReservationView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        if book.stock_quantity > 0:
            Reservation.objects.create(book=book, user=request.user)
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
            "register": request.build_absolute_uri('/register/'),
            "login": request.build_absolute_uri('/login/'),
             "book_statistics": request.build_absolute_uri('/statistics/books/'),
        })


class BookStatisticsView(generics.GenericAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.none()

    def get(self, request, *args, **kwargs):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        popular_books = (
            BookLoan.objects.filter(loan_date__gte=one_year_ago)
            .values('book')
            .annotate(loan_count=Count('id')) 
            .order_by('-loan_count')[:10]  
        )

        response_data = []
        for item in popular_books:
            book = Book.objects.get(id=item['book'])
            response_data.append({
                'title': book.title,
                'author': book.author.name,  
                'loan_count': item['loan_count'],
            })

        return Response(response_data)
