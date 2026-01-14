from django.db import models
 

class Genre(models.Model):
    """
        Represents a movie genre category such as Action, Drama, or Comedy.

        This model is used to classify movies into one or more categories.
        Genres are shared across multiple movies and are
        optimized for fast lookup and filtering.

        Relationships:
            - Many-to-Many with Movie (via MovieGenre)

        Performance:
            - Indexed on `name` for fast genre-based filtering.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Name of the movie genre (e.g., Action, Drama)"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

class Actor(models.Model):
    """
        Represents an actor who has appeared in one or more movies.

        Stores basic biographical information about actors and maintains
        a many-to-many relationship with movies through an explicit
        junction table.

        Relationships:
            - Many-to-Many with Movie (via MovieActor)

        Performance:
            - Indexed on `name` to support fast search and filtering.
    """
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Full name of the actor"
    )
    bio = models.TextField(
        blank=True,
        help_text="Short biography of the actor"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Actor's date of birth"
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Director(models.Model):

    """
        Represents a movie director responsible for directing films.

        Each movie is associated with a single director, while a director
        can be associated with multiple movies.

        Relationships:
            - One-to-Many with Movie

        Performance:
            - Indexed on `name` for efficient director-based queries.
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Full name of the director"
    )
    bio = models.TextField(
        blank=True,
        help_text="Brief biography of the director"
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name



class MovieGenre(models.Model):

    """
        Junction table linking movies and genres.

        This explicit through model enables efficient many-to-many
        relationships between movies and genres while allowing
        fine-grained indexing for performance optimization.

        Relationships:
            - ForeignKey to Movie
            - ForeignKey to Genre

        Constraints:
            - Unique movie-genre pairs enforced.

        Performance:
            - Composite index on (genre, movie) for fast genre filtering.
    """
    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE,
        help_text="Movie associated with this genre"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        help_text="Genre associated with this movie"
    )

    class Meta:
        unique_together = ("movie", "genre")
        indexes = [
            models.Index(fields=["genre", "movie"]),
        ]


class MovieActor(models.Model):
    """
        Junction table linking movies and actors.

        Enables a many-to-many relationship between movies and actors
        with optimized query performance for actor-based filtering.

        Relationships:
            - ForeignKey to Movie
            - ForeignKey to Actor

        Constraints:
            - Prevents duplicate movie-actor associations.

        Performance:
            - Composite index on (actor, movie) to speed up lookups.
    """
    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE,
        help_text="Movie the actor participated in"
    )
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        help_text="Actor involved in the movie"
    )

    class Meta:
        unique_together = ("movie", "actor")
        indexes = [
            models.Index(fields=["actor", "movie"]),
        ]



class Movie(models.Model):
    """
        Represents a movie entity in the platform.

        Stores core metadata such as title, release year, rating, and
        relationships to director, genres, and actors. This model serves
        as the central entity of the movie explorer domain.

        Relationships:
            - ForeignKey to Director (many movies per director)
            - Many-to-Many with Genre (via MovieGenre)
            - Many-to-Many with Actor (via MovieActor)

        Performance:
            - Indexed on title, release_year, and director for fast filtering.
            - Uses explicit through tables for optimized many-to-many queries.
    """
    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Title of the movie"
    )

    release_year = models.PositiveIntegerField(
        db_index=True,
        help_text="Year the movie was released"
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Movie rating (e.g., 8.5)"
    )

    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name="movies",
        db_index=True,
        help_text="Director of the movie"
    )

    genres = models.ManyToManyField(
        Genre,
        through="MovieGenre",
        related_name="movies",
        help_text="Genres associated with the movie"
    )

    actors = models.ManyToManyField(
        Actor,
        through="MovieActor",
        related_name="movies",
        help_text="Actors appearing in the movie"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the movie was added"
    )

    class Meta:
        ordering = ["-release_year", "title"]
        indexes = [
            models.Index(fields=["release_year"]),
            models.Index(fields=["director"]),
            models.Index(fields=["title", "release_year"]),
        ]

    def __str__(self):
        return self.title
