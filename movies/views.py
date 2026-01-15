# REST Framework Imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

# DRF Spectacular Imports
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

# Django Filter Imports
from django_filters.rest_framework import DjangoFilterBackend

# Model Imports
from movies.models import (
    Movie,
    Person,
    Genre,
)

# Serializer Imports
from movies.serializers import (
    MovieSerializer,
    PersonSerializer,
    GenreSerializer,
)

# Filter Imports
from movies.filters import (
    MovieFilter,
    ActorFilter,
    DirectorFilter,
    GenreFilter,
)

# Utility Imports
from utils.pagination import CustomPagination
from utils.validators import validate_query_params


# ================================
# Movie CRUD
# ================================
class MovieViewSet(ModelViewSet):
    """
    Full CRUD operations for Movies.

    Features:
    - Filtering by genre, actor, director, and release year
    - Ordering by title, release_year, rating, or director name
    - Custom pagination with metadata
    - Optimized queries to prevent N+1 issues
    """
    queryset = (
        Movie.objects.prefetch_related(
            "genres",
            "actors",
            "director",
        )
        .distinct()
    )


    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieFilter
    pagination_class = CustomPagination

    ordering_fields = ["title", "release_year", "rating", "director__name"]

    ordering = ["title"]

    allowed_query_params = [
        "genre",
        "actor",
        "director",
        "release_year",
        "page",
        "page_size",
        "ordering",
    ]

    # ---------------- List All ----------------
    @extend_schema(
        summary="List movies",
        description="Paginated list of movies with filtering and ordering.",
        parameters=[
            OpenApiParameter("release_year", OpenApiTypes.INT),
            OpenApiParameter("director", OpenApiTypes.INT),
            OpenApiParameter("genre", OpenApiTypes.INT),
            OpenApiParameter("actor", OpenApiTypes.INT),
        ],
    )
    def list(self, request, *args, **kwargs):
        validate_query_params(
            request, 
            self.allowed_query_params
        )
        return super().list(request, *args, **kwargs)

    # ---------------- Create ----------------
    @extend_schema(
        summary="Create movie",
        description="Create a new movie with actors, directors, and genres."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    # ---------------- Retrieve ----------------
    @extend_schema(
        summary="Retrieve movie",
        description="Retrieve full details of a movie including actors, directors, and genres."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    # ---------------- Update ----------------
    @extend_schema(
        summary="Update movie",
        description="Update an existing movie record."
    )
    def update(self, request, *args, **kwargs):
        print(request.data)
        return super().update(request, *args, **kwargs)
    
    # ---------------- Partial Update ----------------
    @extend_schema(
        summary="Partial update movie",
        description="Update specific fields of a movie."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    # ---------------- Delete ----------------
    @extend_schema(
        summary="Delete movie",
        description="Delete a movie record."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# ================================
# Actor CRUD (Person with Actor Role)
# ================================
class ActorViewSet(ModelViewSet):
    """
    Actor endpoints backed by the Person model.

    Only returns persons who have acted in at least one movie.
    """
    queryset = Person.objects.filter(
        acted_movies__isnull=False
    ).distinct().prefetch_related(
        "acted_movies__genres",
        "acted_movies__director",
    )

    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ActorFilter
    pagination_class = CustomPagination

    ordering_fields = ["name", "date_of_birth"]
    ordering = ["name"]

    allowed_query_params = [
        "movie",
        "name",
        "genre",
        "page",
        "page_size",
        "ordering",
    ]

    @extend_schema(
        summary="List actors",
        description="Paginated list of actors with filtering by movie or genre.",
    )
    def list(self, request, *args, **kwargs):
        validate_query_params(
            request, 
            self.allowed_query_params
        )
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create actor", 
        description="Add a new actor (Person)."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve actor", 
        description="Get details of an actor."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update actor", 
        description="Update an existing actor."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update actor", 
        description="Partial update for actor."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete actor", 
        description="Delete an actor record."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# ================================
# Director CRUD (Person with Director Role)
# ================================
class DirectorViewSet(ModelViewSet):
    """
    Director endpoints backed by the Person model.

    Only returns persons who have directed at least one movie.
    """
    queryset = Person.objects.filter(
        directed_movies__isnull=False
    ).distinct().prefetch_related(
        "directed_movies__actors",
        "directed_movies__genres",
    )

    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DirectorFilter
    pagination_class = CustomPagination

    ordering_fields = ["name"]
    ordering = ["name"]

    allowed_query_params = [
        "movie",
        "name",
        "genre",
        "page",
        "page_size",
        "ordering",
    ]

    @extend_schema(
        summary="List directors",
        description="Paginated list of directors with filtering.",
    )
    def list(self, request, *args, **kwargs):
        validate_query_params(
            request, 
            self.allowed_query_params
        )
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create director", 
        description="Add a new director (Person)."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve director", 
        description="Get details of an director."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update director", 
        description="Update an existing director."
    )
    def update(self, request, *args, **kwargs):
        print(kwargs)
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update director", 
        description="Partial update for director."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete director", 
        description="Delete an actor director."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



# ================================
# Genre CRUD
# ================================
class GenreViewSet(ModelViewSet):
    """
    Full CRUD operations for Genres.
    """
    queryset = Genre.objects.prefetch_related(
        "movies__actors",
        "movies__director",
    )

    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GenreFilter
    pagination_class = CustomPagination

    ordering_fields = ["name"]
    ordering = ["name"]

    allowed_query_params = [
        "movie",
        "name",
        "actor",
        "director",
        "page",
        "page_size",
        "ordering",
    ]

    @extend_schema(
        summary="List genres",
        description="Paginated list of genres with filtering.",
    )
    def list(self, request, *args, **kwargs):
        validate_query_params(
            request, 
            self.allowed_query_params
        )
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create genre", 
        description="Add a new genre."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve genre", 
        description="Get details of an genre."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update genre", 
        description="Update an existing genre."
    )
    def update(self, request, *args, **kwargs):
        print(kwargs)
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update genre", 
        description="Partial update for genre."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete genre", 
        description="Delete an actor genre."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

