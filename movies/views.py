from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import (
    DjangoFilterBackend, 
    OrderingFilter
)

# Model import
from movies.models import (
    Movie, 
    Actor, 
    Director, 
    Genre
)

# Serializer import
from movies.serializers import (
    MovieSerializer, 
    ActorSerializer, 
    DirectorSerializer, 
    GenreSerializer
)

# Filter import
from movies.filters import (
    MovieFilter,
    DirectorFilter,
    ActorFilter,
    GenreFilter
)

# Utility import
from backend.utils.pagination import CustomPagination
from backend.utils.validators import validate_query_params


# ---------------- Movie CRUD ----------------
@extend_schema(
    summary="List all movies",
    description="Returns a paginated list of movies with nested actors, director, and genres. Supports filtering and ordering."
)
class MovieViewSet(ModelViewSet):
    """
    Full CRUD operations for Movies.

    Features:
    - Filtering by genre, actor, director, and release year
    - Ordering by title, release_year, rating, or director name
    - Custom pagination with metadata
    - Optimized queries to prevent N+1
    """
    queryset = Movie.objects.select_related("director").prefetch_related("actors", "genres")
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieFilter
    pagination_class = CustomPagination
    ordering_fields = ["title", "release_year", "rating", "director__name"]
    ordering = ["title"]

    # Allowed query params for this endpoint
    allowed_query_params = [
        "genre", 
        "actor", 
        "director", 
        "release_year", 
        "page", 
        "page_size", 
        "ordering"
    ]

    def list(self, request, *args, **kwargs):
        # Validate query parameters
        validate_query_params(request, self.allowed_query_params)
        return super().list(request, *args, **kwargs)

# ---------------- Actor CRUD ----------------
class ActorViewSet(ModelViewSet):
    """
    Full CRUD operations for Actors.

    Features:
    - Filtering by movies they acted in or genres
    - Ordering by name or date_of_birth
    - Custom pagination
    - Prefetch movies to optimize queries
    - Query parameter validation
    """
    queryset = Actor.objects.prefetch_related("movies__actors", "movies__genres", "movies__director")
    serializer_class = ActorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ActorFilter
    ordering_fields = ["name", "date_of_birth"]
    ordering = ["name"]
    pagination_class = CustomPagination

    # Allowed query params
    allowed_query_params = ["movie", "genre", "page", "page_size", "ordering"]

    def list(self, request, *args, **kwargs):
        validate_query_params(request, self.allowed_query_params)
        return super().list(request, *args, **kwargs)



# ---------------- Director CRUD ----------------
class DirectorViewSet(ModelViewSet):
    """
    Full CRUD operations for Directors.
    """
    queryset = Director.objects.prefetch_related("movies__actors", "movies__genres")
    serializer_class = DirectorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DirectorFilter
    ordering_fields = ["name", "date_of_birth"]
    ordering = ["name"]
    pagination_class = CustomPagination

    allowed_query_params = ["movie", "genre", "page", "page_size", "ordering"]

    def list(self, request, *args, **kwargs):
        validate_query_params(request, self.allowed_query_params)
        return super().list(request, *args, **kwargs)


# ---------------- Genre CRUD ----------------
class GenreViewSet(ModelViewSet):
    """
    Full CRUD operations for Genres.
    """
    queryset = Genre.objects.prefetch_related("movies__actors", "movies__director")
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GenreFilter
    ordering_fields = ["name"]
    ordering = ["name"]
    pagination_class = CustomPagination

    allowed_query_params = ["movie", "actor", "page", "page_size", "ordering"]

    def list(self, request, *args, **kwargs):
        validate_query_params(request, self.allowed_query_params)
        return super().list(request, *args, **kwargs)
