from django import template
register=template.Library()


@register.filter
def get_user(object, user_id):
    return object.get_user(user_id)

@register.filter
def get_doc_items(object, user_id):
    return object.get_doc_items(user_id)

@register.filter
def get_music_items(object, user_id):
    return object.get_music_items(user_id)

@register.filter
def get_photo_items(object, user_id):
    return object.get_music_items(user_id)

@register.filter
def get_video_items(object, user_id):
    return object.get_music_items(user_id)

@register.filter
def get_survey_items(object, user_id):
    return object.get_survey_items(user_id)

@register.filter
def get_elect_new_items(object, user_id):
    return object.get_elect_new_items(user_id)
