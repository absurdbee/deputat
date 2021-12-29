from django import template
import pymorphy2
from string import ascii_letters
register=template.Library()


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False

@register.filter
def rupluralize(value, arg="единица,единицы,единиц"):
    args = arg.split(",")
    if value == '':
        value = 0
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


@register.filter
def is_user_subscribe(elect, user_pk):
    from elect.models import SubscribeElect

    if SubscribeElect.is_elect_subscribe(elect.pk, user_pk):
        return True
    else:
        return False

@register.filter
def item_in_list(list, item_id):
    return list.is_item_in_list(item_id)
@register.filter
def photo_in_media_list(list, item_id):
    return list.is_photo_in_list(item_id)
@register.filter
def video_in_media_list(list, item_id):
    return list.is_video_in_list(item_id)
@register.filter
def track_in_media_list(list, item_id):
    return list.is_track_in_list(item_id)
@register.filter
def doc_in_media_list(list, item_id):
    return list.is_doc_in_list(item_id)

@register.filter
def is_have_item_in_media_list(item, user_id):
    return item.is_item_in_user_media_list(user_id)

@register.filter
def get_attach(obj, request_user):
    return obj.get_u_attach(request_user)
@register.filter
def edit_attach(obj, request_user):
    return obj.get_edit_attach(request_user)

@register.filter
def is_user_can_add_list(list, user_id):
    return list.is_user_can_add_list(user_id)

@register.filter
def is_follower_user(request_user, user_id):
    return request_user.is_followers_user_with_id(user_id)
@register.filter
def is_following_user(request_user, user_id):
    return request_user.is_following_user_with_id(user_id)
@register.filter
def is_blocked_user(user, request_user_id):
    return user.is_blocked_with_user_with_id(request_user_id)
