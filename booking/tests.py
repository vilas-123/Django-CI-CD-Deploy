from django.test import TestCase, Client
from .models import Movie, Booking
import json

class BookingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            name='Avengers',
            total_seats=100
        )

    def test_get_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, 200)

    def test_book_ticket(self):
        response = self.client.post('/api/book/',
            data=json.dumps({
                'movie_id': self.movie.id,
                'user_name': 'John',
                'seats': 2
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_not_enough_seats(self):
        response = self.client.post('/api/book/',
            data=json.dumps({
                'movie_id': self.movie.id,
                'user_name': 'John',
                'seats': 999
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            movie=self.movie,
            user_name='John',
            seats=2
        )
        response = self.client.delete(f'/api/cancel/{booking.id}/')
        self.assertEqual(response.status_code, 200)