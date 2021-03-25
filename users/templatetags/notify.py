from django import template
register=template.Library()

@register.filter
def get_notify(notify, user):
    if user.is_authenticated:
        return notify.get_notify(user)
    else:
        return notify.get_notify(0)
