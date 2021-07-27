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
            'name': socket_name,
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
    #query = Q(object_set__isnull=True)&Q(user_set__isnull=True)
    query = Q(type="BLO", verb="ITE")|Q(type="ELN", verb="ITE")
    query.add(~Q(status="C"), Q.AND)
    return Wall.objects.filter(query)

def get_region_news(name):
    query = Q(type="BLO", verb="ITE")|Q(type="ELN", verb="ITE")
    query.add(~Q(status="C"), Q.AND)
    return Wall.objects.filter(query, verb="ITE")


def get_my_news(user):
    query = Q(creator_id__in=user.get_user_news_notify_ids())|\
            Q(creator_id__in=user.get_user_profile_notify_ids())
    query.add(~Q(status="C"), Q.AND)
    return Wall.objects.filter(query, verb="ITE")

def get_draft_news(user):
    return Wall.objects.filter(verb="SIT")

def get_wall(user, notify):
    # отрисовываем объект стены по его id и типу.
    type = notify.type
    if type == "BLO":
        from common.items.blog import get_wall_blog
        return get_wall_blog(user, notify)
    elif type == "ELN":
        from common.items.elect_new import get_wall_elect_new
        return get_wall_elect_new(user, notify)

def get_notify(user, notify):
    # отрисовываем объект уведомления по его id и типу.
    type = notify.type
    if type == 'BLO':
        from common.items.blog import get_notify_blog
        return get_notify_blog(user, notify)
    elif type == "ELN":
        from common.items.elect_new import get_notify_elect_new
        return get_notify_elect_new(user, notify)
