from django_filters import rest_framework as filters

from .models import (
    Movie,
    Person,
    Genre,
)

# ============================================================
# Movie Filter
# ============================================================
class MovieFilter(filters.FilterSet):
    """
    FilterSet for Movie listings.

    Supports filtering movies by:
    - Genre name
    - Actor name
    - Director name
    - Release year
    """

    genre = filters.CharFilter(
        field_name="genres__name",
        lookup_expr="iexact",
        help_text="Filter movies by exact genre name (case-insensitive)."
    )

    actor = filters.CharFilter(
        field_name="actors__name",
        lookup_expr="icontains",
        help_text="Filter movies by actor name (partial match)."
    )

    director = filters.CharFilter(
        field_name="directors__name",
        lookup_expr="icontains",
        help_text="Filter movies by director name (partial match)."
    )

    release_year = filters.NumberFilter(
        field_name="release_year",
        help_text="Filter movies by release year."
    )

    class Meta:
        model = Movie
        fields = ["genre", "actor", "director", "release_year"]


# ============================================================
# Actors Filte
# ============================================================

class ActorFilter(filters.FilterSet):
    """
    FilterSet for Actor listings.

    Supports filtering actors by:
    - Movie title
    - Movie genre
    """
    movie = filters.CharFilter(
        field_name="acted_movies__title", 
        lookup_expr="icontains"
    )

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    genre = filters.CharFilter(
        field_name="acted_movies__genres__name", 
        lookup_expr="iexact"
    )

    class Meta:
        model = Person
        fields = ["movie", "name", "genre"]

# ============================================================
# Directors Filter
# ============================================================
class DirectorFilter(filters.FilterSet):
    """
    FilterSet for Director listings.

    Supports filtering directors by:
    - Movie title
    - Movie genre
    """

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    movie = filters.CharFilter(
        field_name="directed_movies__title", 
        lookup_expr="icontains"
    )

    genre = filters.CharFilter(
        field_name="directed_movies__genres__name", 
        lookup_expr="iexact"
    )

    class Meta:
        model = Person
        fields = ["movie", "name", "genre"]

# ============================================================
# Genre Filter
# ============================================================
class GenreFilter(filters.FilterSet):
    """
    FilterSet for Genre listings.

    Supports filtering genres by:
    - Movie title
    - Actor name
    """

    movie = filters.CharFilter(
        field_name="movies__title",
        lookup_expr="icontains",
        help_text="Filter genres by movie title."
    )

    actor = filters.CharFilter(
        field_name="movies__actors__name",
        lookup_expr="icontains",
        help_text="Filter genres by actor name."
    )

    class Meta:
        model = Genre
        fields = ["movie", "actor"]
