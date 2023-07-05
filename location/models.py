from django.db import models
from django.contrib.gis.db import models as geo
from django.contrib.auth.models import User


class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=221)
    lat = models.FloatField()
    long = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location {self.id} - {self.user}"


class LocationGeo(geo.Model):
    point = geo.PointField()

    def __str__(self):
        return f"Location {self.id}"
