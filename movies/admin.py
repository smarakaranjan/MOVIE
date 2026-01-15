from django.contrib import admin

# ============================================================
# Model Import
# ============================================================
from .models import (
    Movie,
    Person,
    Genre,
    MovieActor,
    MovieDirector,
    MovieGenre,
)

# ============================================================
# Inlines for Through Tables
# ============================================================

class MovieActorInline(admin.TabularInline):
    """
    Inline to manage actors of a movie using the MovieActor through table.
    Supports character names and autocomplete for actors.
    """
    model = MovieActor
    extra = 1
    autocomplete_fields = ["person"]
    verbose_name = "Actor"
    verbose_name_plural = "Actors"


class MovieDirectorInline(admin.TabularInline):
    """
    Inline to manage directors of a movie using the MovieDirector through table.
    """
    model = MovieDirector
    extra = 1
    autocomplete_fields = ["person"]
    verbose_name = "Director"
    verbose_name_plural = "Directors"


class MovieGenreInline(admin.TabularInline):
    """
    Inline to manage genres of a movie using the MovieGenre through table.
    """
    model = MovieGenre
    extra = 1
    autocomplete_fields = ["genre"]
    verbose_name = "Genre"
    verbose_name_plural = "Genres"


# ============================================================
# Movie Admin
# ============================================================

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin interface for Movie model.

    Features:
    - Display title, release year, rating
    - Search by title, actors, directors
    - Filter by genres, release year
    - Manage actors, directors, and genres inline
    """
    list_display = ("title", "release_year", "rating")
    search_fields = ("title", "actors__person__name", "directors__person__name")
    list_filter = ("release_year", "genres")
    ordering = ("-release_year", "title")
    inlines = [MovieActorInline, MovieDirectorInline, MovieGenreInline]
    autocomplete_fields = []


# ============================================================
# Person Admin
# ============================================================

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin interface for Person model.

    Represents actors, directors, or both.
    """
    list_display = ("name", "date_of_birth")
    search_fields = ("name",)
    ordering = ("name",)


# ============================================================
# Genre Admin
# ============================================================

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin interface for Genre model.
    """
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# ============================================================
# Optional: Admin for Through Tables
# ============================================================

@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    """
    Admin interface for MovieActor through table.
    Allows managing actor–movie relationships with character names.
    """
    list_display = ("movie", "person", "character_name")
    search_fields = ("movie__title", "person__name")
    autocomplete_fields = ["movie", "person"]


@admin.register(MovieDirector)
class MovieDirectorAdmin(admin.ModelAdmin):
    """
    Admin interface for MovieDirector through table.
    """
    list_display = ("movie", "person")
    search_fields = ("movie__title", "person__name")
    autocomplete_fields = ["movie", "person"]


@admin.register(MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    """
    Admin interface for MovieGenre through table.
    """
    list_display = ("movie", "genre")
    search_fields = ("movie__title", "genre__name")
    autocomplete_fields = ["movie", "genre"]
