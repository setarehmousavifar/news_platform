from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied as DjangoPermissionDenied
from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """
    Normalize API errors into a consistent JSON shape:
    {"detail": "...", "errors": {...optional...}}
    Never leaks stack traces (DEBUG handled by Django/DRF separately).
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        data = response.data
        if isinstance(data, dict) and 'detail' in data:
            payload = {'detail': data['detail']}
            extras = {k: v for k, v in data.items() if k != 'detail'}
            if extras:
                payload['errors'] = extras
        elif isinstance(data, dict):
            payload = {'detail': 'Validation failed.', 'errors': data}
        elif isinstance(data, list):
            payload = {'detail': data[0] if data else 'Request failed.', 'errors': data}
        else:
            payload = {'detail': str(data)}
        response.data = payload
        return response

    if isinstance(exc, Http404):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, DjangoPermissionDenied):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            return Response(
                {'detail': 'Validation failed.', 'errors': exc.message_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': '; '.join(exc.messages)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, IntegrityError):
        return Response(
            {'detail': 'Database integrity error. Check unique constraints.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return None
