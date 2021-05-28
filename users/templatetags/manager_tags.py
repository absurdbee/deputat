from django import template
register=template.Library()


@register.filter
def get_user(object):
    return object.get_user()

@register.filter
def get_doc_items(object):
    return object.get_doc_items()

@register.filter
def get_music_items(object):
    return object.get_music_items()

@register.filter
def get_photo_items(object):
    return object.get_photo_items()

@register.filter
def get_video_items(object):
    return object.get_video_items()

@register.filter
def get_survey_items(object):
    return object.get_survey_items()

@register.filter
def get_elect_new_items(object):
    return object.get_elect_new_items()
