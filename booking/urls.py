from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.get_movies),
    path('book/', views.book_ticket),
    path('cancel/<int:booking_id>/', views.cancel_booking),
]