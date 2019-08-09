from django.db import models
from django.urls import reverse


# Create your models here.
class Measurements(models.Model):
    """Model representing a Measurements"""
    timestamp = models.DateTimeField(primary_key=True)
    temperature = models.FloatField()
    dewPoint = models.FloatField()
    precipitation = models.FloatField()

    def __str__(self):
        """Measurements information """
        return self.timestamp

    def get_absoulte_url(self):
        """return the url to access a detail record for the symbol."""
        return reverse('measurements', args=[str(self.timestamp)])
