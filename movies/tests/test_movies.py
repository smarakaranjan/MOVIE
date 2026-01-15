# from rest_framework import status
# from rest_framework.test import APITestCase
# from movies.models import Movie, Person, Genre, MovieActor, MovieGenre

# class MovieTests(APITestCase):
#     def setUp(self):
#         # Create Persons
#         self.actor1 = Person.objects.create(name="Robert Downey Jr.")
#         self.actor2 = Person.objects.create(name="Chris Evans")
#         self.director = Person.objects.create(name="Christopher Nolan")

#         # Create Genres
#         self.genre1 = Genre.objects.create(name="Action")
#         self.genre2 = Genre.objects.create(name="Sci-Fi")

#         # Create a Movie
#         self.movie = Movie.objects.create(
#             title="Original Movie",
#             release_year=2020,
#             rating=8.0,
#             director=self.director
#         )
#         # Link actors
#         MovieActor.objects.create(movie=self.movie, person=self.actor1, character_name="Hero")
#         MovieActor.objects.create(movie=self.movie, person=self.actor2, character_name="Sidekick")
#         # Link genres
#         MovieGenre.objects.create(movie=self.movie, genre=self.genre1)
#         MovieGenre.objects.create(movie=self.movie, genre=self.genre2)

#     def test_create_movie(self):
#         payload = {
#             "title": "Inception",
#             "release_year": 2010,
#             "rating": 8.8,
#             "actors": [
#                 {"person_id": self.actor1.id, "character_name": "Cobb"},
#                 {"person_id": self.actor2.id, "character_name": "Arthur"}
#             ],
#             "director_id": self.director.id,
#             "genres": [
#                 {"genre_id": self.genre1.id},
#                 {"genre_id": self.genre2.id}
#             ]
#         }
#         response = self.client.post("/api/movies/", payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         data = response.json()
#         self.assertEqual(data["title"], "Inception")
#         self.assertEqual(data["release_year"], 2010)
#         self.assertEqual(data["director_info"]["id"], self.director.id)
#         self.assertEqual(len(data["actors_info"]), 2)
#         self.assertEqual(len(data["genres_info"]), 2)

#     def test_list_movies(self):
#         response = self.client.get("/api/movies/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertTrue(len(data["results"]) >= 1)

#     def test_retrieve_movie(self):
#         response = self.client.get(f"/api/movies/{self.movie.id}/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["title"], "Original Movie")
#         self.assertEqual(data["director_info"]["id"], self.director.id)

#     def test_update_movie(self):
#         payload = {
#             "title": "Updated Movie",
#             "release_year": 2024,
#             "rating": 9.0
#         }
#         response = self.client.patch(f"/api/movies/{self.movie.id}/", payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         self.movie.refresh_from_db()
#         self.assertEqual(self.movie.title, "Updated Movie")
#         self.assertEqual(self.movie.release_year, 2024)
#         self.assertEqual(self.movie.rating, 9.0)

#     def test_delete_movie(self):
#         response = self.client.delete(f"/api/movies/{self.movie.id}/")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Movie.objects.filter(id=self.movie.id).exists())

#     def test_partial_update_movie_director(self):
#         # Create a new director
#         new_director = Person.objects.create(name="Steven Spielberg")
#         payload = {"director_id": new_director.id}
#         response = self.client.patch(f"/api/movies/{self.movie.id}/", payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         self.movie.refresh_from_db()
#         self.assertEqual(self.movie.director.id, new_director.id)

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from movies.models import Movie, Person, Genre

class MovieTests(TestCase):
    """Test suite for Movie API endpoints."""

    def setUp(self):
        self.client = APIClient()

        # Create sample persons
        self.actor_1 = Person.objects.create(name="Actor One")
        self.actor_2 = Person.objects.create(name="Actor Two")
        self.director = Person.objects.create(name="Director One")

        # Create sample genres
        self.genre_action = Genre.objects.create(name="Action")
        self.genre_drama = Genre.objects.create(name="Drama")

        # Create sample movie
        self.movie = Movie.objects.create(
            title="Original Movie",
            release_year=2022,
            rating=8.0,
            director=self.director
        )
        self.movie.actors.add(self.actor_1)
        self.movie.genres.add(self.genre_action)

    # ---------------- List ----------------
    def test_list_movies(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Original Movie", [m["title"] for m in response.data['results']])

    # ---------------- Create ----------------
    def test_create_movie(self):
        payload = {
            "title": "Inception",
            "release_year": 2010,
            "rating": 8.8,
            "director_id": self.director.id,
            "actors": [
                {"person_id": self.actor_1.id, "character_name": "Cobb"},
                {"person_id": self.actor_2.id, "character_name": "Arthur"}
            ],
            "genres": [
                {"genre_id": self.genre_action.id},
                {"genre_id": self.genre_drama.id}
            ]
        }
        response = self.client.post("/api/movies/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Movie.objects.filter(title="Inception").exists())

    # ---------------- Retrieve ----------------
    def test_retrieve_movie(self):
        response = self.client.get(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Original Movie")

    # ---------------- Update ----------------
    def test_update_movie(self):
        payload = {
            "title": "Updated Movie",
            "release_year": 2024
        }
        response = self.client.patch(f"/api/movies/{self.movie.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Updated Movie")
        self.assertEqual(self.movie.release_year, 2024)

    # ---------------- Delete ----------------
    def test_delete_movie(self):
        response = self.client.delete(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(id=self.movie.id).exists())

    # ---------------- Filter by genre ----------------
    def test_filter_movies_by_genre(self):
        response = self.client.get(f"/api/movies/?genre={self.genre_action.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.movie.title, [m["title"] for m in response.data['results']])

    # ---------------- Filter by actor ----------------
    def test_filter_movies_by_actor(self):
        response = self.client.get(f"/api/movies/?actor={self.actor_1.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.movie.title, [m["title"] for m in response.data['results']])

    # ---------------- Filter by director ----------------
    def test_filter_movies_by_director(self):
        response = self.client.get(f"/api/movies/?director={self.director.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.movie.title, [m["title"] for m in response.data['results']])

    # ---------------- Filter by release year ----------------
    def test_filter_movies_by_release_year(self):
        response = self.client.get(f"/api/movies/?release_year={self.movie.release_year}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.movie.title, [m["title"] for m in response.data['results']])

    # ---------------- Edge case: nonexistent genre ----------------
    def test_filter_movies_by_nonexistent_genre(self):
        response = self.client.get("/api/movies/?genre=Nonexistent")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
