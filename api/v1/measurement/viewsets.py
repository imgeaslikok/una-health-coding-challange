import os
import json
import pandas as pd
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from utils import responses
from utils.validation import validate_datetime

from measurement import models
from api.v1.measurement import serializers


class GlucoseLevelViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """
        Viewset to return GlucoseLevel data with only List and Retrieve methods
    """

    queryset = models.GlucoseLevel.objects.all()
    serializer_class = serializers.GlucoseLevelSerializer
    ordering_fields = ["value", "timestamp"]

    def get_queryset(self):
        """
            Allows to filter by user_id, start and stop dates
        """
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")

        start = self.request.query_params.get("start")
        stop = self.request.query_params.get("stop")

        if user_id:
            queryset = queryset.filter(user_id=user_id)
            # handle invalid user_id param
            if not queryset:
                raise ValidationError("Invalid user_id")

        # handle invalid datetime
        if start and not validate_datetime(start):
            raise ValidationError("Invalid datetime")
        
        if stop and not validate_datetime(stop):
            raise ValidationError("Invalid datetime")
        
        # filter by date
        if start and stop:
            queryset = queryset.filter(timestamp__range=[start, stop])
        elif start:
            queryset = queryset.filter(timestamp__gte=start)
        elif stop:
            queryset = queryset.filter(timestamp__lte=stop)
            
        return queryset

    def create(self, request, *args, **kwargs):
        """
            Populates GlucoseLevel model from csv files
        """
        files = [f for f in os.listdir(settings.MEDIA_ROOT) if f.endswith(".csv")]
        # handle empty media folder
        if not files:
            return responses.http_no_content_with_details("No CSV files found in media folder")
        try:
            data = []
            for file in files:
                file_path = os.path.join(settings.MEDIA_ROOT, file)
                df = pd.read_csv(file_path)
                df = df[df['Glukosewert-Verlauf mg/dL'].notnull()]
                for _, row in df.iterrows():
                    data.append(
                        models.GlucoseLevel(
                            user_id = file.split(".")[0],
                            device = row["Gerät"],
                            serial_number = row["Seriennummer"],
                            recording_type = row["Aufzeichnungstyp"],
                            value = row["Glukosewert-Verlauf mg/dL"],
                            timestamp = datetime.strptime(row["Gerätezeitstempel"], "%d-%m-%Y %H:%M")
                        )
                    )
            if data:
                models.GlucoseLevel.objects.bulk_create(data)
            return responses.http_created_with_details(f"Successfully imported {len(data)} glucose level measurements")
        
        except Exception as e:
            return responses.http_internal_server_error_with_details(str(e))
        
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        """
            Exports GlucoseLevel model as json
        """
        data = self.serializer_class(self.get_queryset(), many=True).data
        response = HttpResponse(
            content_type="application/json"
        )
        response['Content-Disposition'] = 'attachment; filename="glucose_levels.json"'
        response.write(json.dumps(data, indent=4))
        return response
