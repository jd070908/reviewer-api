from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet, MovieViewSet, ReviewViewSet, 
    ReportViewSet, RegisterView, UserAdminViewSet, CustomApiRoot
)

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'users-admin', UserAdminViewSet, basename='useradmin') # <- Añadimos basename='useradmin'

urlpatterns = [
    path('', CustomApiRoot.as_view(), name='api-root'),
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='auth_register'),
]