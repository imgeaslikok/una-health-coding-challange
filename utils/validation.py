from django.utils.dateparse import parse_datetime


def validate_datetime(datetime_str):
    dt = parse_datetime(datetime_str)
    if not dt:
        return False
    return True
