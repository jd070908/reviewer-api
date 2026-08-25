from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, MovieViewSet, ReviewViewSet, RegisterView

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    # Incluimos las rutas automáticas del router (genres, movies, reviews)
    path('', include(router.urls)),
    
    # Nueva ruta para que cualquier usuario pueda registrarse
    path('register/', RegisterView.as_view(), name='auth_register'),
]