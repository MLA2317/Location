from django.urls import path
from .views import RegisterCreateAPI, LoginCreateApi, CityViewSet, LocationViewSet


urlpatterns = [
    path('register/', RegisterCreateAPI.as_view()),
    path('login/', LoginCreateApi.as_view()),
    path('city_viewset_closest-people/', CityViewSet.as_view({'get': 'list'})),
    path('location/', LocationViewSet.as_view({'post': 'list'})),
]
