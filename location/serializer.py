from rest_framework import serializers
from .models import Location, LocationGeo


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


class SearchSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=220)
    lon = serializers.FloatField(required=True)
    lat = serializers.FloatField(required=True)

    class Meta:
        modul = Location
        fields = ('id', 'city', 'lon', 'lat')
