from django import template
register=template.Library()


@register.filter
def get_user(object, object_id):
    return object.get_user(object_id)

@register.filter
def get_doc_items(object, object_id):
    return object.get_doc_items(object_id)

@register.filter
def get_music_items(object, object_id):
    return object.get_music_items(object_id)

@register.filter
def get_photo_items(object, object_id):
    return object.get_photo_items(object_id)

@register.filter
def get_video_items(object, object_id):
    return object.get_music_items(object_id)

@register.filter
def get_survey_items(object, object_id):
    return object.get_survey_items(object_id)

@register.filter
def get_elect_new_items(object, object_id):
    return object.get_elect_new_items(object_id)
