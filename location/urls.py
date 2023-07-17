from django.urls import path
from .views import RegisterCreateAPI, LoginCreateApi, LocationView


urlpatterns = [
    path('register/', RegisterCreateAPI.as_view()),
    path('login/', LoginCreateApi.as_view()),
    path('closest-people/', LocationView.as_view(), name='closest_people'),
]
