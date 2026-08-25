from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, MovieViewSet, ReviewViewSet, ReportViewSet, RegisterView

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'reports', ReportViewSet)  # Nueva ruta para el sistema de denuncias

urlpatterns = [
    # Incluimos las rutas automáticas del router (genres, movies, reviews, reports)
    path('', include(router.urls)),
    
    # Ruta para que cualquier usuario pueda registrarse
    path('register/', RegisterView.as_view(), name='auth_register'),
]