from rest_framework import serializers
from .models import HealthQuery

class HealthQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthQuery
        fields = "__all__"
