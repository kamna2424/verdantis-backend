from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# PLANT MODEL
# -----------------------------
class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    # Ideal conditions
    ideal_temp_min = models.FloatField(default=20)
    ideal_temp_max = models.FloatField(default=30)

    ideal_humidity_min = models.FloatField(default=40)
    ideal_humidity_max = models.FloatField(default=70)

    ideal_moisture_min = models.FloatField(default=30)
    ideal_moisture_max = models.FloatField(default=60)

    def __str__(self):
        return self.name


# -----------------------------
# SENSOR DATA MODEL
# -----------------------------
class SensorData(models.Model):
    related_name="sensor_readings"
    moisture = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional: link reading to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.plant.name} - {self.timestamp}"
