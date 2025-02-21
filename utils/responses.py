from rest_framework import status
from rest_framework.response import Response

DETAILS_KEY = "details"


def http_not_found_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_404_NOT_FOUND)


def http_no_content_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_204_NO_CONTENT)


def http_ok_with_dict(dict_response=None):
    if dict_response:
        return Response(dict_response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


def http_created_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_201_CREATED)


def http_bad_request_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_400_BAD_REQUEST)


def http_forbidden_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_403_FORBIDDEN)


def http_internal_server_error_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
