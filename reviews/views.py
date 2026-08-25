from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Genre, Movie, Review
from .serializers import GenreSerializer, MovieSerializer, ReviewSerializer, RegisterSerializer
import openai

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genre']
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'title']

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        movie = self.get_object()
        reviews = movie.reviews.all()

        if not reviews.exists():
            return Response({"detail": "Esta película aún no tiene reseñas para resumir."}, status=400)

        reviews_text = "\n".join([f"- {r.comment} (Calificación: {r.rating}/5)" for r in reviews])

        client = openai.OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

        try:
            response = client.chat.completions.create(
                model="llama3",
                messages=[
                    {"role": "system", "content": "Eres un crítico de cine experto. Resume las siguientes reseñas de usuarios en un párrafo corto."},
                    {"role": "user", "content": f"Reseñas para la película '{movie.title}':\n{reviews_text}"}
                ],
                max_tokens=150
            )
            ai_summary = response.choices[0].message.content
            return Response({"movie": movie.title, "ai_summary": ai_summary})
            
        except Exception as e:
            return Response({
                "error": f"No se pudo conectar con Ollama localmente. Asegúrate de que esté abierto. Detalle: {str(e)}"
            }, status=500)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = Movie.objects.none() # No requiere un queryset de películas, usa el de User por defecto en el serializer
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # Permite que cualquier usuario anónimo pueda registrarse