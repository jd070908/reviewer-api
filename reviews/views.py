from rest_framework import viewsets, generics, permissions, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Genre, Movie, Review, Report
from .serializers import (
    GenreSerializer, MovieSerializer, ReviewSerializer, 
    RegisterSerializer, ReportSerializer, BanReportActionSerializer,
    UnbanUserActionSerializer
)
import openai

class IsAdminOrReadOnly(BasePermission):
    """
    Permite lectura (GET, HEAD, OPTIONS) a cualquier usuario,
    pero las modificaciones (POST, PUT, PATCH, DELETE) solo a administradores (is_staff).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsAdminUserOnly(BasePermission):
    """
    Permite el acceso completo únicamente a usuarios administradores (is_staff).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class CustomApiRoot(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response({
            "genres": reverse('genre-list', request=request, format=format),
            "movies": reverse('movie-list', request=request, format=format),
            "reviews": reverse('review-list', request=request, format=format),
            "reports": reverse('report-list', request=request, format=format),
            "users-admin": reverse('useradmin-list', request=request, format=format),
            "register": reverse('auth_register', request=request, format=format),
        })

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]  # Lectura pública, escritura solo admin

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]  # Lectura pública, escritura solo admin
    
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

class ReportActionSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True, help_text="Motivo por el cual se reporta la reseña.")

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], serializer_class=ReportActionSerializer)
    def report(self, request, pk=None):
        """
        Permite a cualquier usuario autenticado reportar una reseña específica directamente desde su endpoint.
        """
        review = self.get_object()
        
        # Validamos los datos de entrada con el serializador de la acción
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data.get('reason')

        # Evitamos reportes duplicados del mismo usuario para la misma reseña
        existing_report = Report.objects.filter(review=review, user=request.user).first()
        if existing_report:
            return Response({"detail": "Ya has reportado esta reseña anteriormente."}, status=400)

        Report.objects.create(
            review=review,
            user=request.user,
            reason=reason
        )

        return Response({"detail": "Reseña reportada con éxito. Los administradores la revisarán."}, status=201)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUserOnly]  # Exclusivo para administradores

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], serializer_class=BanReportActionSerializer)
    def delete_review(self, request, pk=None):
        report = self.get_object()
        review = report.review
        author = review.user  
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ban_user = serializer.validated_data.get('ban_user', False)
        
        response_data = {}

        report.is_resolved = True
        report.save()
        response_data["report_detail"] = "Reporte marcado como resuelto."

        if review:
            review.delete()
            response_data["review_detail"] = "Reseña eliminada con éxito."

        if ban_user and author:
            author.is_active = False  
            author.save()
            response_data["user_detail"] = f"El usuario {author.username} ha sido baneado (desactivado)."
        else:
            response_data["user_detail"] = "El usuario se mantiene activo."

        return Response(response_data)

class RegisterView(generics.CreateAPIView):
    queryset = Movie.objects.none() 
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class UserAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet para que los administradores puedan ver la lista de usuarios 
    y desbanearlos (reactivar su cuenta).
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUserOnly]  # Exclusivo para administradores
    lookup_field = 'username'

    @action(detail=True, methods=['post'], serializer_class=UnbanUserActionSerializer)
    def unban_user(self, request, username=None):
        user = self.get_object()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user.is_active = True
        user.save()
        
        return Response({
            "detail": f"El usuario {user.username} ha sido desbaneado y reactivado con éxito."
        })