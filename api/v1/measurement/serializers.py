from rest_framework import serializers

from measurement import models


class GlucoseLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GlucoseLevel
        fields = "__all__"
