from django.contrib import admin
from .models import Author, Genre, Book, BookLoan, Reservation

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'nationality')
    search_fields = ('name',)
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_date', 'stock_quantity')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genre', 'publication_date')

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'loan_date', 'return_date', 'is_active')
    search_fields = ('user__username', 'book__title')
    list_filter = ('loan_date',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'reservation_date', 'is_active')
    search_fields = ('user__username', 'book__title')
    list_filter = ('reservation_date',)
