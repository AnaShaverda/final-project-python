from rest_framework import serializers
from .models import CustomUser, Author, Genre, Book, BookLoan  # Assuming BookLoan is your reservation model

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'personal_number', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            personal_number=validated_data['personal_number'],
            birth_date=validated_data['birth_date']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'nationality']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']  

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'publication_date'] 

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan  
        fields = ['id', 'book', 'user', 'loan_date', 'return_date']  
