from django.db import models
from django.utils import timezone

class VisitorLog(models.Model):
    date = models.DateField(default=timezone.now)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.count}"
