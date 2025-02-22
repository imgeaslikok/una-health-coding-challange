import os
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from io import StringIO
from django.conf import settings
from measurement import models

class GlucoseLevelCSVPopulateTest(APITestCase):
    """
        Test cases for GlucoseLevelViewset POST method that 
        populates data from CSV and stores it in model
    """
    def setUp(self):
        self.url = "/api/v1/levels/"
        models.GlucoseLevel.objects.all().delete()  # Clean up any existing data
        self.dummy_csv_content = "Gerät,Seriennummer,Aufzeichnungstyp,Glukosewert-Verlauf mg/dL,Gerätezeitstempel\n" \
                                  "Device A,123456,0,100,25-02-2021 10:30\n" \
                                  "Device B,123457,0,120,26-02-2021 11:45\n"

    @patch("os.listdir") # Mocking os.listdir to avoid real file system interaction
    @patch("pandas.read_csv") # Mocking pandas.read_csv to avoid reading actual files
    def test_create_glucose_levels_from_csv(self, mock_read_csv, mock_listdir):
        # Mocking the list of files returned by os.listdir to simulate CSV files in the media folder
        mock_listdir.return_value = ["user1.csv"]
        # Mocking the pandas read_csv to return a dataframe with the dummy CSV content
        mock_df = pd.read_csv(StringIO(self.dummy_csv_content))
        mock_read_csv.return_value = mock_df

        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("os.listdir")
    def test_create_no_csv_files(self, mock_listdir):
        mock_listdir.return_value = []
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(response.data["details"], "No CSV files found in media folder")


class GlucoseLevelViewsetTest(APITestCase):
    """
        Test cases for GlucoseLevelViewset GET methods
    """
    def setUp(self):
        self.url = "/api/v1/levels/"
        models.GlucoseLevel.objects.all().delete()
        self.glucose_level1 = models.GlucoseLevel.objects.create(
            user_id="user1",
            device="Device A",
            serial_number="123456",
            recording_type="0",
            value=100,
            timestamp=datetime(2021, 2, 25, 10, 30)
        )
        self.glucose_level2 = models.GlucoseLevel.objects.create(
            user_id="user1",
            device="Device B",
            serial_number="123457",
            recording_type="0",
            value=120,
            timestamp=datetime(2021, 2, 26, 11, 45)
        )
        self.glucose_level3 = models.GlucoseLevel.objects.create(
            user_id="user2",
            device="Device C",
            serial_number="123458",
            recording_type="0",
            value=110,
            timestamp=datetime(2021, 2, 27, 14, 0)
        )

    def test_get_levels(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_get_levels_by_user(self):
        response = self.client.get(self.url + "?user_id=user1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_levels_by_filtering_start_date(self):
        response = self.client.get(self.url + "?start=2021-02-26T11:45:00Z")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_levels_by_filtering_stop_date(self):
        response = self.client.get(self.url + "?stop=2021-02-25T11:45:00Z")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_levels_by_filtering_start_and_stop_date(self):
        response = self.client.get(self.url + "?start=2021-02-26T11:45:00Z&stop=2021-02-27T15:45:00Z")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
