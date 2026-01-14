from django.contrib import admin
from .models import Movie, Actor, Director, Genre

# ------------------------------
# Movie Admin
# ------------------------------
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin interface for Movie model.

    Displays key fields, enables filtering by director, year, and genres,
    search by title, and horizontal filters for actors and genres.
    """
    list_display = ("title", "release_year", "director", "rating")
    list_filter = ("release_year", "director", "genres")
    search_fields = ("title", "director__name", "actors__name")
    filter_horizontal = ("genres", "actors")


# ------------------------------
# Actor Admin
# ------------------------------
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """
    Admin interface for Actor model.

    Allows searching by name, filtering by movies they acted in,
    and displaying associated movies inline.
    """
    list_display = ("name", "date_of_birth")
    search_fields = ("name", "movies__title")
    list_filter = ("movies",)
    filter_horizontal = ("movies",)


# ------------------------------
# Director Admin
# ------------------------------
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    """
    Admin interface for Director model.

    Allows filtering by movies directed, searching by director name.
    """
    list_display = ("name",)
    search_fields = ("name", "movies__title")
    list_filter = ("movies",)
    filter_horizontal = ("movies",)


# ------------------------------
# Genre Admin
# ------------------------------
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin interface for Genre model.

    Allows filtering by movies in this genre and searching by genre name.
    """
    list_display = ("name",)
    search_fields = ("name", "movies__title")
    list_filter = ("movies",)
    filter_horizontal = ("movies",)
