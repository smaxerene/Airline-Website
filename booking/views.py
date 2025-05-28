from django.shortcuts import render, get_object_or_404, redirect
from .models import ScheduledFlight, Booking
import random, string
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import F

def home(request):
    # Get all valid flights where origin ≠ destination
    flights = list(
        ScheduledFlight.objects.exclude(origin__city=F('destination__city')).order_by('departure_time')
    )

    if flights:
        earliest_departure = flights[0].departure_time.date()
        today = now().date()
        day_diff = (today - earliest_departure).days

        for flight in flights:
            if day_diff > 0:
                flight.departure_time += timedelta(days=day_diff)

    return render(request, "booking/home.html", {"flights": flights})

def book_flight(request, flight_id):
    flight = get_object_or_404(ScheduledFlight, id=flight_id)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        if not name or not email:
            error = "Please provide both name and email."
            return render(request, "booking/book.html", {"flight": flight, "error": error})
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        Booking.objects.create(scheduled_flight=flight, customer_name=name, customer_email=email, reference_code=ref)
        return render(request, "booking/confirmation.html", {"ref": ref, "flight": flight,  "name": name, "email": email})
    return render(request, "booking/book.html", {"flight": flight})

def booking_confirmation(request, ref, flight_id, name, email):
    flight = get_object_or_404(ScheduledFlight, pk=flight_id)
    return render(request, "booking/confirmation.html", {
        "ref": ref,
        "flight": flight,
        "name": name,
        "email": email
    })

def search_flights(request):
    origin = request.GET.get("origin", "")
    destination = request.GET.get("destination", "")
    results = []

    if origin and destination:
        results = ScheduledFlight.objects.filter(
            origin__city__icontains=origin,
            destination__city__icontains=destination
        )

    return render(request, "booking/search_results.html", {
        "results": results,
        "query": f"{origin} to {destination}"
    })

def cancel_view(request):
    bookings = []
    email = None

    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST['email']
        bookings = Booking.objects.filter(customer_email=email)

    return render(request, 'booking/cancel.html', {'email': email, 'bookings': bookings})

def confirm_cancel(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)