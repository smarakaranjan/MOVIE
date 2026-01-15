from django.db import models


# ============================================================
# Genre
# ============================================================

class Genre(models.Model):
    """
    Represents a movie genre such as Action, Drama, Comedy, or Thriller.

    Genres are shared reference data used to classify movies.
    A movie can belong to multiple genres, and a genre can be
    associated with multiple movies.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique genre name (e.g., Action, Drama, Comedy)"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


# ============================================================
# Person
# ============================================================

class Person(models.Model):
    """
    Represents a person involved in movie production.

    A single person can perform multiple roles such as:
    - Actor
    - Director
    - Both Actor and Director

    Role information is derived from relationship tables
    (MovieActor) instead of a fixed role field,
    allowing maximum flexibility and normalization.
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Full legal or stage name of the person"
    )

    bio = models.TextField(
        blank=True,
        help_text="Short biography or career summary"
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth (optional)"
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


# ============================================================
# Movie
# ============================================================

class Movie(models.Model):
    """
    Core domain model representing a movie.

    Stores basic movie metadata and manages relationships to:
    - Genres
    - Actors
    - Directors

    Uses explicit through tables for many-to-many relationships
    to support future extensibility and optimized querying.
    """

    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Official title of the movie"
    )

    release_year = models.PositiveIntegerField(
        db_index=True,
        help_text="Year in which the movie was released"
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Average movie rating (e.g., 8.5)"
    )

    genres = models.ManyToManyField(
        Genre,
        through="MovieGenre",
        related_name="movies",
        help_text="Genres associated with this movie"
    )

    actors = models.ManyToManyField(
        Person,

        through="MovieActor",
        related_name="acted_movies",
        help_text="Actors who appeared in this movie"
    )

    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="directed_movies",
        null=True,
        help_text="Director of the movie"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the movie record was created"
    )

    class Meta:
        ordering = ["-release_year", "title"]
        indexes = [
            models.Index(fields=["release_year"]),
            models.Index(fields=["title", "release_year"]),
        ]

    def __str__(self):
        return self.title


# ============================================================
# Through Tables
# ============================================================

class MovieGenre(models.Model):
    """
    Junction table connecting movies and genres.

    This explicit table allows:
    - Enforcing uniqueness of movie-genre pairs
    - Efficient filtering by genre
    - Future extension (e.g., primary genre flag)
    """

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        help_text="Movie associated with the genre"
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        help_text="Genre assigned to the movie"
    )

    class Meta:
        unique_together = ("movie", "genre")
        indexes = [
            models.Index(fields=["genre", "movie"]),
        ]

    def __str__(self):
        return f"{self.movie} → {self.genre}"


class MovieActor(models.Model):
    """
    Junction table linking actors (persons) to movies.

    Stores actor-specific metadata such as character names.
    Enables a normalized and extensible actor–movie relationship.
    """

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        help_text="Movie in which the actor appeared"
    )

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="Person who acted in the movie"
    )

    character_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of the character played by the actor"
    )

    class Meta:
        unique_together = ("movie", "person")
        indexes = [
            models.Index(fields=["person", "movie"]),
        ]

    def __str__(self):
        return f"{self.person} in {self.movie}"


 