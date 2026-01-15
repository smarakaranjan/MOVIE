from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from movies.models import Person, Movie, Genre


class ActorTests(TestCase):
    """Comprehensive test suite for Actor API endpoints."""

    def setUp(self):
        self.client = APIClient()

        # ---------------- Sample Data ----------------
        # Actors
        self.actor_1 = Person.objects.create(name="Actor One")
        self.actor_2 = Person.objects.create(name="Actor Two")

        # Directors
        self.director_1 = Person.objects.create(name="Director One")
        self.director_2 = Person.objects.create(name="Director Two")

        # Genres
        self.genre_action = Genre.objects.create(name="Action")
        self.genre_drama = Genre.objects.create(name="Drama")

        # Movies
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
    def test_list_actors(self):
        response = self.client.get("/api/actors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [a["name"] for a in response.data.get('results', response.data)]
        self.assertIn("Actor One", names)
        self.assertIn("Actor Two", names)

    # ---------------- Create ----------------
    def test_create_actor(self):
        payload = {"name": "New Actor"}
        response = self.client.post("/api/actors/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Person.objects.filter(name="New Actor").exists())

    # ---------------- Retrieve ----------------
    def test_retrieve_actor(self):
        response = self.client.get(f"/api/actors/{self.actor_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Actor One")

    # ---------------- Update ----------------
    def test_update_actor(self):
        payload = {"name": "Actor Updated"}
        response = self.client.patch(f"/api/actors/{self.actor_2.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.actor_2.refresh_from_db()
        self.assertEqual(self.actor_2.name, "Actor Updated")

    # ---------------- Delete ----------------
    def test_delete_actor(self):
        response = self.client.delete(f"/api/actors/{self.actor_2.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Person.objects.filter(id=self.actor_2.id).exists())

    # ---------------- Filter by movie ----------------
    def test_filter_actors_by_movie(self):
        response = self.client.get(f"/api/actors/?movie={self.movie_1.title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [a["name"] for a in response.data.get('results', response.data)]
        self.assertIn("Actor One", names)
        self.assertNotIn("Actor Two", names)

    # ---------------- Filter by genre ----------------
    def test_filter_actors_by_genre(self):
        response = self.client.get(f"/api/actors/?genre=Action")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [a["name"] for a in response.data.get('results', response.data)]
        self.assertIn("Actor One", names)
        self.assertNotIn("Actor Two", names)

    # ---------------- Edge case: non-existent movie ----------------
    def test_filter_actors_by_nonexistent_movie(self):
        response = self.client.get("/api/actors/?movie=Nonexistent Movie")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', response.data)), 0)

    # ---------------- Edge case: non-existent genre ----------------
    def test_filter_actors_by_nonexistent_genre(self):
        response = self.client.get("/api/actors/?genre=Nonexistent Genre")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', response.data)), 0)

    # ---------------- Edge case: invalid query parameter ----------------
    def test_invalid_filter_param(self):
        response = self.client.get("/api/actors/?foo=bar")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid query parameters", str(response.data))

     
