from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    personal_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username  

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.name 

class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name  

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title 

    def is_available(self):
        """Check if the book is available for loan."""
        return self.stock_quantity > 0

class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book.title}"

    def is_active(self):
        """Check if the loan is still active."""
        return self.return_date is None

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} reserved {self.book.title}"

    def deactivate(self):
        """Deactivate the reservation."""
        self.is_active = False
        self.save()
