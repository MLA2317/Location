from django.urls import path
from .views import RegisterCreateAPI, LoginCreateApi


urlpatterns = [
    path('register/', RegisterCreateAPI.as_view()),
    path('login/', LoginCreateApi.as_view())
]
