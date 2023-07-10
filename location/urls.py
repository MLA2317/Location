from django.urls import path
from .views import RegisterCreateAPI, LoginCreateApi, ClosestPeopleView


urlpatterns = [
    path('register/', RegisterCreateAPI.as_view()),
    path('login/', LoginCreateApi.as_view()),
    path('closest-people/<int:city_id>/', ClosestPeopleView.as_view(), name='closest_people'),
]
