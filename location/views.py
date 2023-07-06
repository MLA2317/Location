from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import Location
from .serializer import RegisterSerializer, LoginSerializer, LocationSerializer, ClosestPeopleSerializer


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


class ClosestPeopleView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get closest people",
        responses={200: LocationSerializer(many=True)},
    )
    def get(self, request, location_id):
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=404)

        serializer = LocationSerializer(location)
        return Response(serializer.data)





# class SearchLocationCreateApi(generics.ListCreateAPIView):
#     serializer_class = SearchSerializer
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





