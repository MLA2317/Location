from rest_framework import serializers
from .models import Location, LocationGeo
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=25, write_only=True)
    password2 = serializers.CharField(max_length=25, write_only=True)

    class Meta:
        model = Location
        fields = ['username', 'password', 'password2', 'city', 'lat', 'long', 'created_date']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise ValueError('Password didnt match')
        print('attrs', attrs)
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Location.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Location
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username != password:
            raise ValueError('Username or Password wrong!')

        return attrs


class ClosestPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'username', 'city', 'lat', 'long']


class LocationSerializer(serializers.ModelSerializer):
    closest_people = serializers.SerializerMethodField()

    def get_closest_people(self, obj):
        radius = 1000
        points = Point(obj.long, obj.lat)
        closest_locations = Location.objects.exclude(id=obj.id).annotate(distance=Distance('point', points)).order_by('distance')[:5]
        serializer = ClosestPeopleSerializer(closest_locations, many=True)
        return serializer.data

    class Meta:
        model = Location
        fields = ['id', 'username', 'city', 'lat', 'long', 'closest_people']





# class ClosestPeopleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = ['lat', 'long']
#
#
# class LocationSerializer(serializers.ModelSerializer):
#     closest_people = serializers.SerializerMethodField()
#
#     def get_closest_people(self, obj):
#         latitude = obj.latitude
#         longitude = obj.longitude
#         radius = 1000  # Berilgan radiusni o'zingizga mos ravishda o'zgartirishingiz mumkin
#
#         point = Point(longitude, latitude)
#
#         closest_locations = Location.objects.filter(coordinates__distance_lte=(point, Distance(m=radius))) \
#                              .exclude(id=obj.id) \
#                              .annotate(distance=Distance('coordinates', point)) \
#                              .order_by('distance')[:5]  # Eng yaqin 5 ta odamni tanlab olish
#
#         serializer = ClosestPeopleSerializer(closest_locations, many=True)
#         return serializer.data
#
#     class Meta:
#         model = Location
#         fields = ['id', 'latitude', 'longitude', 'closest_people']
#
#

# class SearchSerializer(serializers.ModelSerializer):
#     city = serializers.CharField(max_length=220)
#     distance = serializers.DecimalField(source='distance.km', max_digits=10, decimal_places=2, required=False, read_only=True)
#     lon = serializers.FloatField(required=True)
#     lat = serializers.FloatField(required=True)
#
#     class Meta:
#         model = Location
#         fields = ('city', 'distance', 'lon', 'lat')
