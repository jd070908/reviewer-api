from rest_framework import serializers
from .models import Genre, Movie, Review

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    # Esto es para que en el JSON veamos el nombre del usuario en lugar de solo su ID
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user'] # El usuario se asignará automáticamente en la vista

class MovieSerializer(serializers.ModelSerializer):
    # Esto permite anidar: al ver la película, verás también su género y sus reseñas
    genre = GenreSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genre', 'reviews']