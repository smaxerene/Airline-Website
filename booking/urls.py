from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:flight_id>/', views.book_flight, name='book'),
    path('confirmation/<str:ref>/<int:flight_id>/', views.booking_confirmation, name='confirmation'),
    path('search/', views.search_flights, name='search_flights'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('cancel/<int:booking_id>/', views.confirm_cancel, name='confirm_cancel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)