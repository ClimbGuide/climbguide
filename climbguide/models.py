from django.db import models
from django.db.models import Q, Count
from mapbox_location_field.models import LocationField, AddressAutoHiddenField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from users.models import User
import string


class Route(models.Model):
    mountainproject_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    route_type = models.CharField(max_length=100, null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    mp_stars = models.IntegerField()
    pitches = models.CharField(max_length=100, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class PoiQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.is_authenticated:
            pois = self.filter(Q(public=True) | Q(owner=user))
        else:
            pois = self.filter(public=True)
        return pois

class Pointofinterest(models.Model):
    objects = PoiQuerySet.as_manager()

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="pointsofinterest", null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    information = models.CharField(max_length=250, null=True, blank=True)
    longitude = models.FloatField(null=False, blank=True, default=1)
    latitude = models.FloatField(null=False, blank=True, default=1)
    location = models.OneToOneField(to="Location", related_name='pointofinterest',null=True, blank=True, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)   
    public = models.BooleanField(default=True)
    HANGOUT = "HG"
    PARKING = "PG"
    TRAILHEAD = "TH"
    VIEWPOINT = "VP"
    CATEGORY_CHOICES = [
        (HANGOUT, "Hangout Spot"),
        (PARKING, "Parking"),
        (TRAILHEAD, "Trailhead"),
        (VIEWPOINT, "Viewpoint"),
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=HANGOUT)
    
class Location(models.Model):
    location = LocationField(map_attrs={"style":"mapbox://styles/mapbox/streets-v11","center": (-80.793457, 35.782169),"zoom":5})


class DaytripQuerySet(models.QuerySet):
    def count_routes(self):
        daytrips = self.annotate(
            num_routes=Count("routes", distinct=True)
        )
        return daytrips


class Daytrip(models.Model):
    objects = DaytripQuerySet.as_manager()

    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    owners = models.ManyToManyField(to=User, related_name="daytrips", blank=True)
    routes = models.ManyToManyField(to=Route, related_name="daytrips", blank=True)
    points_of_interest = models.ManyToManyField(to=Pointofinterest, related_name="daytrips", blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Log(models.Model):
    text = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    daytrip = models.ForeignKey(to=Daytrip, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    point_of_interest = models.ForeignKey(to=Pointofinterest, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)


class Star(models.Model):
    stars = models.IntegerField()
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="stars", null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="stars", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
    photo = models.ImageField(upload_to="routephotos/", null=True, blank=True)
    photo_thumb = ImageSpecField(source="photo", processors=[ResizeToFill(200,200)], format="JPEG", options={"quality": 80})
    photo_large = ImageSpecField(source="photo", processors=[ResizeToFit(400,400)], format="JPEG", options={"quality": 80})
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)
    point_of_interest = models.ForeignKey(to=Pointofinterest, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


def clean_location(self):
    locations = self.strip('][').split(', ')
    cleaned_locations = []
    for location in locations:
        clean_location = location.strip("'")
        cleaned_locations.append(clean_location)
    return cleaned_locations 
                
                