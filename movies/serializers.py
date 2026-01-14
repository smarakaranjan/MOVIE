from rest_framework import serializers
from .models import Movie, Actor, Director, Genre

################## Readable Serializer ####################

# ---------------- Actor Nested Serializer ----------------
class ActorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "name")


# ---------------- Director Nested Serializer ----------------
class DirectorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("id", "name")


# ---------------- Genre Nested Serializer ----------------
class GenreNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


# ---------------- Movie Serializer ----------------
class MovieSerializer(serializers.ModelSerializer):
    """
    Movie serializer for full CRUD.
    - Read: nested actors, director, genres
    - Write: accepts IDs for actors, director, genres
    """

    # Nested read-only for frontend
    actors = ActorNestedSerializer(many=True, read_only=True)
    genres = GenreNestedSerializer(many=True, read_only=True)
    director = DirectorNestedSerializer(read_only=True)

    # Write-only fields for POST/PUT
    actor_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all(),
        write_only=True,
        source="actors"
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        write_only=True,
        source="genres"
    )
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(),
        write_only=True,
        source="director"
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "release_year",
            "rating",
            "description",
            "actors",
            "genres",
            "director",
            "actor_ids",
            "genre_ids",
            "director_id"
        ]


# ---------------- Actor Serializers -------------- #

class ActorSerializer(serializers.ModelSerializer):
    """
    Actor serializer:
    - Read: movies nested
    - Write: standard fields
    """
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ["id", "name", "date_of_birth", "movies"]



class DirectorSerializer(serializers.ModelSerializer):
    """
    Director serializer:
    - Read: movies nested
    """
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Director
        fields = ["id", "name", "date_of_birth", "movies"]

# ---------------- Genre Serializer ----------------
class GenreSerializer(serializers.ModelSerializer):
    """
    Genre Serializer:

    - Read: Returns nested movies, each including actors and director
    - Write: Accepts list of movie IDs for assigning movies to genre
    """

    movies = MovieSerializer(many=True, read_only=True)
    movie_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Movie.objects.all(),
        source="movies"  # link to M2M field in Genre model
    )

    class Meta:
        model = Genre
        fields = ["id", "name", "movies", "movie_ids"]