from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ActorViewSet, DirectorViewSet, GenreViewSet

# Create a DRF router
router = DefaultRouter()
router.register(r"", MovieViewSet, basename="movie")
router.register(r"actors", ActorViewSet, basename="actor")
router.register(r"directors", DirectorViewSet, basename="director")
router.register(r"genres", GenreViewSet, basename="genre")

urlpatterns = [
    path("", include(router.urls)),
]
