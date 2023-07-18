from django.contrib.gis.geos import GEOSGeometry

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response
from .models import Location, City
from .serializer import RegisterSerializer, LoginSerializer, CitySerializer, LocationSerializer


class RegisterCreateAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': 'Successfully created'}, status=status.HTTP_201_CREATED)


class LoginCreateApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully log in'}, status=status.HTTP_201_CREATED)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    # print('queryset', queryset)
    serializer_class = LocationSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_nearest_cities(self, city):
        if city.location_geo:
            print('location', city.location_geo)
            return City.objects.exclude(id=city.id).annotate(distance=Distance('location_geo__point', city.location_geo.point)).order_by('distance')[:5]
        return City.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance', instance)
        serializer = self.get_serializer(instance)
        print('serializer', serializer)
        nearest_cities = self.get_nearest_cities(instance)
        nearest_cities_serializer = self.get_serializer(nearest_cities, many=True)
        data = serializer.data
        data['nearest_cities'] = nearest_cities_serializer.data
        return Response(data)


# class LocationView(generics.CreateAPIView):
#     serializer_class = LocationSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             lat = serializer.validated_data.get('lat')
#             long = serializer.validated_data.get('long')
#
#             point = Point(long, lat, srid=4326)
#             print('point', point)
#
#             cities = City.objects.annotate(distance=Distance('location_geo__point', point)).order_by('distance')[:5]
#             print('cities', cities)
#
#             city_data = []
#             for city in cities:
#                 city_data.append({
#                     'id': city.id,
#                     'name': city.title,
#                     'distance': city.distance.km,
#                 })
#
#             return Response(city_data)
#         else:
#             return Response(serializer.errors, status=400)
#
# #
#


# class ClosestPeopleView(views.APIView):
#     queryset = Location.objects.all()
#     serializer_class = CitySerializer
#
#     @swagger_auto_schema(
#         operation_description="Get closest people",
#         responses={200: City(many=True)},
#         manual_parameters=[
#             openapi.Parameter(
#                 name='city_id',
#                 in_=openapi.IN_PATH,
#                 description='Location ID',
#                 type=openapi.TYPE_INTEGER,
#             ),
#         ]
#     )
#     def get_closest_people(self, obj):
#         location_geo = obj.location_geo
#         print('loca', location_geo)
#         closest_locations = Location.objects.exclude(id=location_geo.location.id).annotate(
#             distance=Distance('geo__point', location_geo.point)
#         ).order_by('distance')[:5]
#         print('closest people', closest_locations)
#         serializer = CitySerializer(closest_locations, many=True)
#         return Response({'success', True, 'message', serializer.data}, status=status.HTTP_200_OK)

    # class Meta:
    #     model = City
    #     fields = ['id', 'title', 'location_geo']


# class SearchLocationCreateApi(generics.ListCreateAPIView):
#     serializer_class = LocationSerializer
#
#     def get_queryset(self, *args, **kwargs):
#         latitude = self.request.query_params.get('lat', 0)
#         longitude = self.request.query_params.get('long', 0)
#         radius = self.request.query_params.get('rad', 0)
#
#         if latitude and longitude:
#
#             pnt = GEOSGeometry('POINT(' + str(latitude) + ' ' + str(longitude) + ')', srid=4326)
#
#             for locat in Location.objects.annotate(distance=Distance('coordinates', pnt)):
#                 diss = locat.distance.km
#                 if float(radius) > float(diss):
#                     locat_dis = list(Location.objects.annotate(distance=Distance(
#                         'coordinates', pnt)).order_by('distance').order_by(
#                         'distance').filter(distance__lte=float(radius) * 1000))
#                     return locat_dis



# class LocationView(views.APIView):
#     def post(self, request):
#         serializer = CitySerializer(data=request.data)
#         if serializer.is_valid():
#             lat = serializer.validated_data['lat']
#             long = serializer.validated_data['long']
#
#             point = Point(long, lat, srid=4326)
#
#             cities = City.objects.annotate(distance=Distance('location', point)).order_by('distance')[:5]
#
#             city_data = []
#             for city in cities:
#                 print('city', city)
#                 city_data.append({
#                     'id': city.id,
#                     'name': city.title,
#                     'distance': city.distance.km,
#                 })
#                 print('city_data', city_data)
#
#             return Response(city_data)
#         else:
#             return Response(serializer.errors, status=400)

