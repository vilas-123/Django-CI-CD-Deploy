from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movie, Booking
import json

def get_movies(request):
    movies = list(Movie.objects.values())
    return JsonResponse(movies, safe=False)

@csrf_exempt
def book_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            movie = Movie.objects.get(id=data['movie_id'])

            if movie.total_seats < data['seats']:
                return JsonResponse({'error': 'Not enough seats'}, status=400)

            movie.total_seats -= data['seats']
            movie.save()

            booking = Booking.objects.create(
                movie=movie,
                user_name=data['user_name'],
                seats=data['seats']
            )
            return JsonResponse({
                'message': 'Booking successful',
                'booking_id': booking.id
            })

        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def cancel_booking(request, booking_id):
    if request.method == 'DELETE':
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.movie.total_seats += booking.seats
            booking.movie.save()
            booking.delete()
            return JsonResponse({'message': 'Booking cancelled'})
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=405)