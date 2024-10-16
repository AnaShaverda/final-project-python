from django.urls import path
from .views import (
    loan_book,
    loan_success,
    UserRegistrationView,
    AuthorViewSet,
    GenreViewSet,
    BookViewSet,
    BookListView, 
    ReservationView, 
    RootView
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
     path('', RootView.as_view(), name='api-root'),
    path('loan/<int:book_id>/', loan_book, name='loan_book'),
    path('loan/success/', loan_success, name='loan_success'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('books/', BookListView.as_view(), name='book-list'),  
    path('reserve/<int:book_id>/', ReservationView.as_view(), name='reserve-book'), 
    
]

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)

urlpatterns += router.urls