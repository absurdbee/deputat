from django import template
register=template.Library()


@register.filter
def get_user(object, user_id):
    return object.get_user(user_id)
