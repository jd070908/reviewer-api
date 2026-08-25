from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Genre, Movie, Review, Report

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

class RegisterSerializer(serializers.ModelSerializer):
    # Configuramos la contraseña para que sea de "solo escritura" por seguridad
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Usamos create_user para que la contraseña se guarde encriptada (hasheada) correctamente
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class ReportSerializer(serializers.ModelSerializer):
    # Campos informativos de solo lectura para la API
    username = serializers.ReadOnlyField(source='user.username')
    review_comment = serializers.ReadOnlyField(source='review.comment')
    review_owner = serializers.ReadOnlyField(source='review.user.username')

    class Meta:
        model = Report
        fields = ['id', 'review', 'user', 'username', 'review_comment', 'review_owner', 'reason', 'created_at', 'is_resolved']
        read_only_fields = ['user', 'created_at']