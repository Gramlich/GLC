from django.db import models
from jsonfield import JSONField
from django.urls import reverse

class Document(models.Model):
    data = models.FileField(upload_to='documents/')


class WorkOut(models.Model):
    boat = models.CharField(default='N/A', max_length=40)
    date = models.CharField(default='N/A', max_length=40)
    time = models.CharField(default='N/A', max_length=40)
    session_type = models.CharField(default='N/A', max_length=40)
    speed_input = models.CharField(default='N/A', max_length=40)
    total_distance = models.CharField(default='N/A', max_length=6)
    distance_from_start = JSONField(max_length=10, default=dict)

    total_time = models.CharField(default='N/A', max_length=15)
    avg_stroke_rate = models.CharField(default='N/A', max_length=6)
    avg_split = models.CharField(default='N/A', max_length=6)
    avg_speed = models.CharField(default='N/A', max_length=6)


    stroke_rate = JSONField(max_length=10, default=dict)
    elapsed_time = JSONField(max_length=10, default=dict)
    split = JSONField(max_length=10, default=dict)
    speed = JSONField(max_length=10, default=dict)
    distance_per_stroke = JSONField(max_length=10, default=dict)

    slug = models.SlugField(unique=True, max_length=40)

    def __str__(self):
        return self.boat + ' ' + self.date + ' ' + self.time

    def get_absolute_url(self):
        return reverse('workout_graph', kwargs={'slug': self.slug})

