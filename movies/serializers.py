from django.db import transaction
from rest_framework import serializers

from .models import (
    Movie, 
    Person, 
    Genre, 
    MovieActor,  
    MovieGenre
)

# ============================================================
# Genre Serializer
# ============================================================

class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model.

    Represents a movie genre such as Action, Drama, or Comedy.

    Fields:
        - id: Primary key of the genre
        - name: Name of the genre
    """
    class Meta:
        model = Genre
        fields = ["id", "name"]


# ============================================================
# Person Serializer
# ============================================================

class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Person model.

    Represents an individual involved in movie production.
    Can be an actor, director, or both.

    Fields:
        - id: Primary key of the person
        - name: Full legal or stage name
        - bio: Short biography or career summary
        - date_of_birth: Date of birth (optional)
    """
    class Meta:
        model = Person
        fields = ["id", "name", "bio", "date_of_birth", "image_url"]


class ActorListSerializer(serializers.ModelSerializer):
    """
    Serializer for Actor list view with movies.
    """
    movies = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = ["id", "name", "bio", "date_of_birth", "image_url", "movies"]
    
    def get_movies(self, obj):
        """Get movies where this person acted"""
        movies = obj.acted_movies.all()[:6]  # Limit to 6 movies for list view
        return [
            {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "rating": movie.rating,
                "image_url": movie.image_url,
            }
            for movie in movies
        ]


class DirectorListSerializer(serializers.ModelSerializer):
    """
    Serializer for Director list view with movies.
    """
    movies = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = ["id", "name", "bio", "date_of_birth", "image_url", "movies"]
    
    def get_movies(self, obj):
        """Get movies directed by this person"""
        movies = obj.directed_movies.all()[:6]  # Limit to 6 movies for list view
        return [
            {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "rating": movie.rating,
                "image_url": movie.image_url,
            }
            for movie in movies
        ]


class ActorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Actor detail view with initial movies and pagination info.
    """
    movies = serializers.SerializerMethodField()
    movies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = ["id", "name", "bio", "date_of_birth", "image_url", "movies", "movies_count"]
    
    def get_movies(self, obj):
        """Get initial movies where this person acted (first 12)"""
        movies = obj.acted_movies.all().order_by('-release_year')[:12]
        return [
            {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "rating": movie.rating,
                "image_url": movie.image_url,
            }
            for movie in movies
        ]
    
    def get_movies_count(self, obj):
        """Get total count of movies"""
        return obj.acted_movies.count()


class DirectorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Director detail view with initial movies and pagination info.
    """
    movies = serializers.SerializerMethodField()
    movies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = ["id", "name", "bio", "date_of_birth", "image_url", "movies", "movies_count"]
    
    def get_movies(self, obj):
        """Get initial movies directed by this person (first 12)"""
        movies = obj.directed_movies.all().order_by('-release_year')[:12]
        return [
            {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "rating": movie.rating,
                "image_url": movie.image_url,
            }
            for movie in movies
        ]
    
    def get_movies_count(self, obj):
        """Get total count of movies"""
        return obj.directed_movies.count()


# ============================================================
# MovieActor Serializer
# ============================================================

class MovieActorSerializer(serializers.ModelSerializer):
    """
    Serializer for the MovieActor through table.

    Represents the relationship between a movie and an actor (Person).

    Fields:
        - id: Primary key of the MovieActor record
        - person: Nested person details (read-only)
        - person_id: ID for assigning actor when creating/updating
        - character_name: Name of the character played in the movie
    """
    person = PersonSerializer(read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        write_only=True,
        source="person",
        help_text="ID of the actor to associate with this movie"
    )

    class Meta:
        model = MovieActor
        fields = ["person", "person_id", "character_name"]


# ============================================================
# MovieGenre Serializer
# ============================================================

class MovieGenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the MovieGenre through table.

    Represents the relationship between a movie and a genre.

    Fields:
        - id: Primary key of the MovieGenre record
        - genre: Nested genre details (read-only)
        - genre_id: ID for assigning genre when creating/updating
    """
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        write_only=True,
        source="genre",
        help_text="ID of the genre to associate with this movie"
    )

    class Meta:
        model = MovieGenre
        fields = ["genre", "genre_id"]


# ============================================================
# Movie Serializers
# ============================================================

class MovieSerializer(serializers.ModelSerializer):
    # ---------- READ ----------
    actors_info = MovieActorSerializer(source="movieactor_set", many=True, read_only=True)
    director_info = PersonSerializer(source="director", read_only=True)
    genres_info = MovieGenreSerializer(source="moviegenre_set", many=True, read_only=True)

    # ---------- WRITE ----------
    actors = MovieActorSerializer(source="movieactor_set", many=True, write_only=True, required=False)
    director_id = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), source="director", write_only=True)
    genres = MovieGenreSerializer(source="moviegenre_set", many=True, write_only=True, required=False)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "release_year",
            "rating",
            "image_url",
            "actors_info",
            "director_info",
            "genres_info",
            "actors",
            "director_info",
            "director_id",
            "genres",
            "created_at",
        ]

    # ---------- Helper ----------
    def _update_m2m(self, instance, model, data_list):
        """
        Generic helper to update through-table relations.
        - None → do nothing (partial update)
        - [] → delete all
        """
        if data_list is None:
            return

        model.objects.filter(movie=instance).delete()
        if not data_list:
            return

        model.objects.bulk_create([model(movie=instance, **item) for item in data_list])

    # ---------- Create ----------
    def create(self, validated_data):
        actors_data = validated_data.pop("movieactor_set", [])
        genres_data = validated_data.pop("moviegenre_set", [])

        with transaction.atomic():
            movie = Movie.objects.create(**validated_data)
            self._update_m2m(movie, MovieActor, actors_data)
            self._update_m2m(movie, MovieGenre, genres_data)

        return movie

    # ---------- Update ----------
    def update(self, instance, validated_data):
        actors_data = validated_data.pop("movieactor_set", None)
        genres_data = validated_data.pop("moviegenre_set", None)

        with transaction.atomic():
            # Update main fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Update nested relations
            self._update_m2m(instance, MovieActor, actors_data)
            self._update_m2m(instance, MovieGenre, genres_data)

        return instance
