from django.db import models
from django.utils import timezone

# Create your models here.

class WeatherQuery(models.Model):
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Weather Query"
        verbose_name_plural = "Weather Queries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.location} ({self.start_date} to {self.end_date})"

    def is_valid_date_range(self):
        """Check if the date range is valid."""
        return self.start_date <= self.end_date

    def save(self, *args, **kwargs):
        if not self.is_valid_date_range():
            raise ValueError("End date must be after or equal to start date")
        super().save(*args, **kwargs)
