from django.db import models

class  Movie(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    seats = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.movie.name}"