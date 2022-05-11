from django.db import models
import datetime
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Hall(models.Model):
    sitRows = models.IntegerField(validators=[MinValueValidator(1)])
    sitColumns = models.IntegerField(
        validators=[MaxValueValidator(20), MinValueValidator(1)])

    def __str__(self):
        return f'Sit Rows {self.sitRows}, sit columns {self.sitColumns}'

    @property
    def numberOfPlaces(self):
        return self.sitRows * self.sitColumns


class Cinema(models.Model):
    name = models.CharField('Cinema Name', max_length=100)
    halls = models.ManyToManyField(Hall)

    def __str__(self):
        return f'Cinema Name: {self.name}'


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

    @property
    def isActive(self):
        return datetime.now() < self.end_time

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
