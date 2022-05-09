from django.db import models
import datetime
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Cinema(models.Model):
    name = models.CharField('Cinema Name', max_length=100)

    def __str__(self):
        return self.name


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    sitPlaces = models.IntegerField()

    def __str__(self):
        return f'Cinema: {self.cinema} hall. Sit Places {self.sitPlaces}'


class Session(models.Model):
    name = models.CharField('Movie Name', max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)
    session_image = models.ImageField(upload_to="images/")
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True)

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError(
                {'end_time': _('End time must be bigger than the start time!')})

    def alreadyPassed(self):
        return datetime.now() > self.end_time

    def __str__(self):
        return self.name


class Place(models.Model):
    placeNumber = models.IntegerField()
    isAvaliable = models.BooleanField()
    placeHolder = models.IntegerField(null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        if self.isAvaliable:
            return f'{self.placeNumber} is available'
        else:
            return f'{self.placeNumber} is taken'
