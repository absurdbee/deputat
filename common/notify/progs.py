from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from notify.models import Notify, Wall

def user_send_notify(id, creator_id, recipient_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, recipient_id - id получателя, socket_name-имя, по которому следует назначать событие в скрипте js
    if creator_id != recipient_id:
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'id': str(id),
            'recipient_id': str(recipient_id),
            'name': "u_post_create",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def community_send_notify(id, creator_id, recipient_id, community_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    if creator_id != recipient_id:
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': str(recipient_id),
            'community_id': str(community_id),
            'creator_community_id': str(action_community_id),
            'id': str(id),
            'name': socket_name,
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


def user_send_wall(id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'community_id': str(action_community_id),
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def community_send_wall(id, creator_id, community_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'community_id': str(community_id),
        'action_community_id': str(action_community_id),
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def get_news():
    # пока исключаем из выдачи группировку "оценил три поста" user_set__isnull=True
    query = Q(object_set__isnull=True)&Q(user_set__isnull=True)
    return Wall.objects.filter(query, verb="ITE")

def get_region_news(name):
    # пока исключаем из выдачи группировку "оценил три поста" user_set__isnull=True
    query = Q(object_set__isnull=True) & Q(options__icontains=name)
    return Wall.objects.filter(query, verb="ITE")


def get_my_news(user):
    query = Q(creator_id__in=user.get_user_news_notify_ids())|\
            Q(creator_id__in=user.get_user_profile_notify_ids())
    query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
    return Wall.objects.filter(query, verb="ITE")

def get_draft_news(user):
    return Wall.objects.filter(verb="SIT")

def get_notify(user, notify):
    type = notify.type
    if type == "BLO":
        from common.items.blog import get_blog
        return get_blog(user, notify)
    elif type == "BLOC":
        from common.items.blog import get_comment_blog
        return get_comment_blog(user, notify)
