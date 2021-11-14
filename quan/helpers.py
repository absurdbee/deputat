def validate_file_extension(value):
    from rest_framework.exceptions import ValidationError
    from django.conf import settings

    if value.size > settings.DOC_FILE_MAX_SIZE:
        raise ValidationError('Размер не более 5 МБ!')
