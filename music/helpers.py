import uuid
from os.path import splitext


def upload_to_music_directory(user_profile, filename):
    creator = user_profile.creator
    return _upload_to_user_directory(creator=creator, filename=filename)

def _upload_to_user_directory(creator, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension

    path = 'users/%(user_uuid)s/music/' % {
        'user_uuid': str(creator.id)}

    return '%(path)s%(new_filename)s' % {'path': path,
                                         'new_filename': new_filename, }

def validate_file_extension(value):
    import os
    from django.http import HttpResponse
    from django.conf import settings

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.ogg','.mp3','.wav']
    if not ext in valid_extensions:
        return HttpResponse('Допустимы форматы: ogg, mp3, wav!')
    if value.size > settings.MUSIC_FILE_MAX_SIZE:
        return HttpResponse('Размер не более 5 МБ!')
