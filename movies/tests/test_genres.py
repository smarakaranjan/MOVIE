# movies/tests/test_genres.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from movies.models import Genre, Movie, Person

class GenreTests(TestCase):
    """Test suite for Genre API endpoints."""

    def setUp(self):
        self.client = APIClient()

        # Sample actors
        self.actor_1 = Person.objects.create(name="Actor One")
        self.actor_2 = Person.objects.create(name="Actor Two")

        # Sample directors
        self.director_1 = Person.objects.create(name="Director One")
        self.director_2 = Person.objects.create(name="Director Two")

        # Sample genres
        self.genre_action = Genre.objects.create(name="Action")
        self.genre_drama = Genre.objects.create(name="Drama")

        # Sample movies
        self.movie_1 = Movie.objects.create(
            title="Movie One",
            release_year=2022,
            rating=8.0,
            director=self.director_1
        )
        self.movie_1.actors.add(self.actor_1)
        self.movie_1.genres.add(self.genre_action)

        self.movie_2 = Movie.objects.create(
            title="Movie Two",
            release_year=2023,
            rating=7.5,
            director=self.director_2
        )
        self.movie_2.actors.add(self.actor_2)
        self.movie_2.genres.add(self.genre_drama)

    # ---------------- List ----------------
    def test_list_genres(self):
        response = self.client.get("/api/genres/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [g["name"] for g in response.data['results']]
        self.assertIn("Action", names)
        self.assertIn("Drama", names)

    # ---------------- Create ----------------
    def test_create_genre(self):
        payload = {"name": "Comedy"}
        response = self.client.post("/api/genres/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Genre.objects.filter(name="Comedy").exists())

    # ---------------- Retrieve ----------------
    def test_retrieve_genre(self):
        response = self.client.get(f"/api/genres/{self.genre_action.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Action")

    # ---------------- Update ----------------
    def test_update_genre(self):
        payload = {"name": "Action Updated"}
        response = self.client.patch(f"/api/genres/{self.genre_action.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre_action.refresh_from_db()
        self.assertEqual(self.genre_action.name, "Action Updated")

    # ---------------- Delete ----------------
    def test_delete_genre(self):
        response = self.client.delete(f"/api/genres/{self.genre_drama.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(id=self.genre_drama.id).exists())

    # ---------------- Filter by movie ----------------
    def test_filter_genres_by_movie(self):
        response = self.client.get(f"/api/genres/?movie={self.movie_1.title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Action", [g["name"] for g in response.data['results']])

    # ---------------- Filter by actor ----------------
    def test_filter_genres_by_actor(self):
        response = self.client.get(f"/api/genres/?actor={self.actor_1.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Action", [g["name"] for g in response.data['results']])

    # ---------------- Filter by director ----------------
    def test_filter_genres_by_director(self):
        response = self.client.get(f"/api/genres/?director={self.director_1.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Action", [g["name"] for g in response.data['results']])

    # ---------------- Edge case: non-existent movie ----------------
    def test_filter_genres_by_nonexistent_movie(self):
        response = self.client.get("/api/genres/?movie=Nonexistent Movie")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    # ---------------- Edge case: non-existent actor ----------------
    def test_filter_genres_by_nonexistent_actor(self):
        response = self.client.get("/api/genres/?actor=Nonexistent Actor")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    # ---------------- Edge case: non-existent director ----------------
    def test_filter_genres_by_nonexistent_director(self):
        response = self.client.get("/api/genres/?director=Nonexistent Director")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    # ---------------- Edge case: invalid query param ----------------
    def test_invalid_filter_param(self):
        response = self.client.get("/api/genres/?foo=bar")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid query parameters", str(response.data))
