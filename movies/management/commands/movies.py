import random
from django.core.management.base import BaseCommand
from movies.models import Movie, Person, Genre, MovieActor, MovieGenre

# ----------------------------
# Predefined data
# ----------------------------
MOVIE_TITLES = [
    "Silent Horizon", "Crimson Dawn", "Shadow's Edge", "Fallen Kingdom", "Eternal Flame",
    "Golden Mirage", "Whispering Winds", "Forgotten Path", "Iron Legacy", "Midnight Secrets",
    "Celestial Journey", "Shattered Memories", "Broken Compass", "Distant Echo", "Twilight Veil",
    "Frozen Time", "Hidden Truths", "Burning Skies", "Lost Horizon", "Silver Lining",
    "Secret Passage", "Dark Matter", "Rising Tides", "Lone Star", "Veiled Shadows",
    "Crimson Tide", "Endless Night", "Silent Whisper", "Golden Horizon", "Fading Light",
    "Mystic River", "Shadow Realm", "Fallen Stars", "Hidden Fortress", "Twilight Dreams",
    "Iron Heart", "Forgotten Realm", "Burning Bridges", "Lost Legacy", "Silver Shadows",
    "Secret Garden", "Dark Horizon", "Rising Dawn", "Eternal Night", "Whispering Shadows",
    "Shattered Sky", "Frozen Flame", "Golden Path", "Silent Storm", "Twilight Echo",
    "Celestial Shadows", "Fallen Realm", "Hidden Horizon", "Midnight Mirage", "Iron Veil",
    "Lost Echo", "Mystic Horizon", "Burning Night", "Silver Flame", "Dark Legacy",
    "Crimson Echo", "Twilight Path", "Golden Veil", "Frozen Horizon", "Shadowed Legacy",
    "Whispering Night", "Secret Horizon", "Rising Shadows", "Fading Mirage", "Silent Echo",
    "Hidden Flame", "Eternal Horizon", "Shattered Legacy", "Iron Shadows", "Lost Horizon",
    "Mystic Flame", "Golden Shadow", "Twilight Legacy", "Dark Horizon", "Crimson Path",
    "Frozen Shadows", "Hidden Echo", "Burning Horizon", "Silver Mirage", "Silent Legacy",
    "Shadowed Horizon", "Twilight Flame", "Lost Shadows", "Rising Horizon", "Golden Echo",
    "Eternal Shadows", "Hidden Legacy", "Iron Horizon", "Faded Shadows", "Mystic Legacy",
    "Shattered Horizon", "Silent Flame", "Crimson Horizon", "Twilight Shadows", "Golden Horizon",
    "Frozen Legacy", "Hidden Flame", "Burning Shadows", "Silver Horizon", "Shadowed Flame",
]

ACTOR_NAMES = [
    "Robert Downey Jr.", "Scarlett Johansson", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth",
    "Jennifer Lawrence", "Brad Pitt", "Angelina Jolie", "Leonardo DiCaprio", "Natalie Portman",
    "Tom Hanks", "Meryl Streep", "Morgan Freeman", "Emma Stone", "Ryan Gosling",
    "Gal Gadot", "Henry Cavill", "Zendaya", "Dwayne Johnson", "Margot Robbie",
]

DIRECTOR_NAMES = [
    "Steven Spielberg", "Christopher Nolan", "Quentin Tarantino", "Martin Scorsese", "James Cameron",
    "Peter Jackson", "Ridley Scott", "Alfred Hitchcock", "Francis Ford Coppola", "George Lucas",
]

GENRE_NAMES = [
    "Action", "Adventure", "Drama", "Comedy", "Thriller", "Horror", "Sci-Fi", "Fantasy", "Romance", "Mystery"
]

# ----------------------------
# Command
# ----------------------------
class Command(BaseCommand):
    help = "Populate movies with random genres, actors, and a single director"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating database with movies...")

        # Create Genres
        genres = []
        for name in GENRE_NAMES:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)

        # Create Actors
        actors = []
        for name in ACTOR_NAMES:
            actor, _ = Person.objects.get_or_create(name=name)
            actors.append(actor)

        # Create Directors
        directors = []
        for name in DIRECTOR_NAMES:
            director, _ = Person.objects.get_or_create(name=name)
            directors.append(director)

        # Create Movies
        for i, title in enumerate(MOVIE_TITLES, start=1):
            movie, created = Movie.objects.get_or_create(
                title=title,
                release_year=random.randint(1980, 2025),
                rating=round(random.uniform(5.0, 9.5), 1)
            )

            # Assign exactly 1 random director
            movie.director = random.choice(directors)
            movie.save()

            # Assign 1-3 random genres
            movie_genres = random.sample(genres, k=random.randint(1, 3))
            for genre in movie_genres:
                MovieGenre.objects.get_or_create(movie=movie, genre=genre)

            # Assign 1-4 random actors
            movie_actors = random.sample(actors, k=random.randint(1, 4))
            for actor in movie_actors:
                MovieActor.objects.get_or_create(movie=movie, person=actor, character_name=f"Character {i}")

            self.stdout.write(f"Created movie: {movie.title} (Director: {movie.director.name})")

        self.stdout.write(self.style.SUCCESS("Successfully populated movies!"))
