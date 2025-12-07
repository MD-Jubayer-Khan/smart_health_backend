from django.db import models

# Create your models here.


class HealthQuery(models.Model):
    user_query = models.TextField()
    extracted_symptoms = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_query
