from django.db import models
from django.contrib.gis.db import models as geo
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractUser
from django.db.models.signals import post_save


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError("Password should not be None")

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Location(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name='Username', db_index=True)
    city = models.CharField(max_length=221)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_active = models.BooleanField(default=False, verbose_name='Active user')
    is_staff = models.BooleanField(default=True, verbose_name='Staff user')
    created_date = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Location {self.id} - {self.username}"


class LocationGeo(geo.Model):
    point = geo.PointField()

    def __str__(self):
        return f"Location {self.id}"

    def get_google_map_url(self):
        latitude = self.point.y
        longitude = self.point.x
        url = f"https://www.google.com/maps?q={latitude},{longitude}"
        return url


# class City(models.Model):
#     name = models.CharField(max_length=100)
#     lat = models.FloatField(null=True)
#     long = models.FloatField(null=True)
#
#     def __str__(self):
#         return self.name

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Location.objects.create(user=instance)
#
#
# post_save.connect(create_user_profile, sender=User)
