from django.conf import settings
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_CONTENT_TYPES = {
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',
}

ALLOWED_VIDEO_CONTENT_TYPES = {
    'video/mp4',
    'video/webm',
    'video/quicktime',
}


def validate_image_upload(file):
    if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise ValidationError('Only JPEG, PNG, WebP, and GIF images are allowed.')

    max_size = getattr(settings, 'MAX_IMAGE_UPLOAD_SIZE', 5 * 1024 * 1024)
    if file.size > max_size:
        raise ValidationError(f'Image size must not exceed {max_size // (1024 * 1024)} MB.')


def validate_video_upload(file):
    if file.content_type not in ALLOWED_VIDEO_CONTENT_TYPES:
        raise ValidationError('Only MP4, WebM, and MOV videos are allowed.')

    max_size = getattr(settings, 'MAX_VIDEO_UPLOAD_SIZE', 50 * 1024 * 1024)
    if file.size > max_size:
        raise ValidationError(f'Video size must not exceed {max_size // (1024 * 1024)} MB.')
