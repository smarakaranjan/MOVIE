from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from movies.models import Movie, Person, Genre

class DirectorTests(TestCase):
    """Test CRUD and filtering for Directors"""

    def setUp(self):
        # API client
        self.client = APIClient()

        # Create Genres
        self.genre_action = Genre.objects.create(name="Action")
        self.genre_drama = Genre.objects.create(name="Drama")

        # Create Directors
        self.director_1 = Person.objects.create(name="Director One")
        self.director_2 = Person.objects.create(name="Director Two")

        # Create Actors (optional for filtering)
        self.actor_1 = Person.objects.create(name="Actor One")
        self.actor_2 = Person.objects.create(name="Actor Two")

        # Create Movies
        self.movie = Movie.objects.create(
            title="Action Movie",
            release_year=2023,
            rating=8.0,
            director=self.director_1
        )
        self.movie.genres.add(self.genre_action)
        self.movie2 = Movie.objects.create(
            title="Drama Movie",
            release_year=2022,
            rating=7.5,
            director=self.director_2
        )
        self.movie2.genres.add(self.genre_drama)

    # ---------------- List ----------------
    def test_list_directors(self):
        response = self.client.get("/api/directors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        director_names = [d["name"] for d in response.data['results']]
        self.assertIn(self.director_1.name, director_names)
        self.assertIn(self.director_2.name, director_names)

    # ---------------- Create ----------------
    def test_create_director(self):
        payload = {"name": "New Director"}
        response = self.client.post("/api/directors/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Person.objects.filter(name="New Director").exists())

    # ---------------- Retrieve ----------------
    def test_retrieve_director(self):
        response = self.client.get(f"/api/directors/{self.director_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.director_1.name)

    # ---------------- Update ----------------
    def test_update_director(self):
        payload = {"name": "Updated Director"}
        response = self.client.put(
            f"/api/directors/{self.director_1.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.director_1.refresh_from_db()
        self.assertEqual(self.director_1.name, "Updated Director")

    # ---------------- Partial Update ----------------
    def test_partial_update_director(self):
        payload = {"name": "Partially Updated Director"}
        response = self.client.patch(
            f"/api/directors/{self.director_1.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.director_1.refresh_from_db()
        self.assertEqual(self.director_1.name, "Partially Updated Director")

    # ---------------- Delete ----------------
    def test_delete_director(self):
        response = self.client.delete(f"/api/directors/{self.director_2.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Person.objects.filter(id=self.director_2.id).exists())

    # ---------------- Filtering ----------------
    def test_filter_directors_by_movie(self):
        response = self.client.get(f"/api/directors/?movie=Action Movie")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        director_names = [d["name"] for d in response.data['results']]
        self.assertIn(self.director_1.name, director_names)
        self.assertNotIn(self.director_2.name, director_names)

    def test_filter_directors_by_genre(self):
        response = self.client.get("/api/directors/?genre=Action")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        director_names = [d["name"] for d in response.data['results']]
        self.assertIn(self.director_1.name, director_names)
        self.assertNotIn(self.director_2.name, director_names)
    
    # ---------------- Edge case: invalid movie ----------------
    def test_filter_directors_by_nonexistent_movie(self):
        response = self.client.get("/api/directors/?movie=Nonexistent Movie")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

        # ---------------- Edge case: nonexistent genre ----------------
    def test_filter_directors_by_nonexistent_genre(self):
        response = self.client.get("/api/directors/?genre=Nonexistent")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    # ---------------- Edge case: invalid query param ----------------
    def test_invalid_filter_param(self):
        response = self.client.get("/api/directors/?foo=bar")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid query parameters", str(response.data))


 