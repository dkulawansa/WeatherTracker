from __future__ import unicode_literals
from .views import WeatherTracker, WeatherTrackerDetail
from django.urls import path


urlpatterns = [
    path('measurements', WeatherTracker.as_view()), # for POST
    path('measurements/<str:pk>', WeatherTrackerDetail.as_view()), #to get Details
    path('stats/<str:stat>', WeatherTracker.as_view()),
    path('stats/<str:stat>/<str:metric>', WeatherTracker.as_view()),
    path('stats/<str:stat>/<str:metric>/<str:fromDateTime>', WeatherTracker.as_view()),
    path('stats/<str:stat>/<str:metric>/<str:fromDateTime>/<str:toDateTime>', WeatherTracker.as_view()),

]

