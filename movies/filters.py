import django_filters
from django_filters import rest_framework as filters
from .models import Movie, Actor, Director, Genre

# ---------------- Movie Filter ----------------
class MovieFilter(filters.FilterSet):
    """
    FilterSet for Movies.

    Allows filtering by:
    - genre name
    - actor name
    - director name
    - release year
    """

    genre = filters.CharFilter(field_name="genres__name", lookup_expr="iexact")
    actor = filters.CharFilter(field_name="actors__name", lookup_expr="icontains")
    director = filters.CharFilter(field_name="director__name", lookup_expr="icontains")
    release_year = filters.NumberFilter(field_name="release_year")

    class Meta:
        model = Movie
        fields = ["genre", "actor", "director", "release_year"]


# ---------------- Actor Filter ----------------
class ActorFilter(filters.FilterSet):
    """
    FilterSet for Actors.

    Allows filtering by:
    - movies they acted in
    - genres of those movies
    """

    movie = filters.CharFilter(field_name="movies__title", lookup_expr="icontains")
    genre = filters.CharFilter(field_name="movies__genres__name", lookup_expr="iexact")

    class Meta:
        model = Actor
        fields = ["movie", "genre"]


# ---------------- Director Filter ----------------
class DirectorFilter(filters.FilterSet):
    """
    FilterSet for Directors.

    Allows filtering by:
    - movies they directed
    - genres of those movies
    """

    movie = filters.CharFilter(field_name="movies__title", lookup_expr="icontains")
    genre = filters.CharFilter(field_name="movies__genres__name", lookup_expr="iexact")

    class Meta:
        model = Director
        fields = ["movie", "genre"]


# ---------------- Genre Filter ----------------
class GenreFilter(filters.FilterSet):
    """
    FilterSet for Genres.

    Allows filtering by:
    - movies in this genre
    - actors in those movies
    """

    movie = filters.CharFilter(field_name="movies__title", lookup_expr="icontains")
    actor = filters.CharFilter(field_name="movies__actors__name", lookup_expr="icontains")

    class Meta:
        model = Genre
        fields = ["movie", "actor"]
