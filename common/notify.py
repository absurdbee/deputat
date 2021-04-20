from django.db.models import Q
from notify.models import Notify, Wall


def get_news():
    # пока исключаем из выдачи группировку "оценил три поста" user_set__isnull=True
    query = Q(object_set__isnull=True)&Q(user_set__isnull=True)
    return Wall.objects.filter(query)

def get_region_news(name):
    # пока исключаем из выдачи группировку "оценил три поста" user_set__isnull=True
    query = Q(object_set__isnull=True) & Q(options__icontains=name)
    return Wall.objects.filter(query)


def get_my_news(user):
    query = Q(creator_id__in=user.get_user_news_notify_ids())|\
            Q(creator_id__in=user.get_user_profile_notify_ids())
    query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
    return Wall.objects.filter(query)

def get_draft_news(user):
    query = Q(verb="SIT") & Q(user_set__isnull=True, object_set__isnull=True)
    return Wall.objects.filter(query)

def user_notify(creator, type, object_id, socket_name, verb):
    from notify.models import Notify
    from datetime import date 

    current_verb, today = creator.get_verb_gender(verb), date.today()
    for user_id in creator.get_member_for_notify_ids():
        if Notify.objects.filter(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=verb).exists():
            pass
        elif Notify.objects.filter(recipient_id=user_id, created__gt=today, type=type, verb=current_verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, type=type, created__gt=today, verb=current_verb).last()
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb, user_set=notify)
        elif Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).last()
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb)
            send_notify_socket(attach[3:], user_id, socket_name)

def user_wall(creator, type, object_id, socket_name, verb):
    from notify.models import Wall
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()

    if Wall.objects.filter(creator_id=creator.pk, object_id=object_id, type=type, verb=verb).exists():
        pass
    if Wall.objects.filter(created__gt=today, type=type, verb=current_verb).exists():
        notify = Wall.objects.filter(type=type, created__gt=today, verb=current_verb).last()
        Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb=current_verb, user_set=notify)
    elif Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).exists():
        notify = Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).last()
        Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
    else:
        Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb=current_verb)
    send_wall_socket(attach[3:], socket_name)


def get_notify(user, notify):
    type = notify.type
    if type == "BLO":
        from common.items.blog import get_blog
        return get_blog(user, notify)
    elif type == "BLOC":
        from common.items.blog import get_comment_blog
        return get_comment_blog(user, notify)

def user_comment_notify(creator, object_id, type, socket_name, verb):
    from notify.models import Notify
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()
    for user_id in creator.get_member_for_notify_ids():
        if Notify.objects.filter(recipient_id=user_id, created__gt=today, type=type, verb=current_verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, type=type, created__gt=today, verb=current_verb).last()
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb, user_set=notify)
        elif Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).last()
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb)
            send_notify_socket(attach[3:], user_id, socket_name)

def user_comment_wall(creator, object_id, type, socket_name, verb):
    from notify.models import Wall
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()
    if Wall.objects.filter(created__gt=today, type=type, verb=current_verb).exists():
        notify = Wall.objects.filter(type=type, created__gt=today, verb=current_verb).last()
        wall = Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb=current_verb, user_set=notify)
    elif Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).exists():
        notify = Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).last()
        wall = Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
    else:
        wall = Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb=current_verb)
    send_wall_socket(wall.pk, socket_name)


def send_notify_socket(id, recipient_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, user_ids-все получатели уведомлений, recipient_id - id получателя,
    # socket_name-имя, по которому следует назначать событие в скрипте js
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'id': str(post.pk),
        'recipient_id': str(recipient_id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def send_wall_socket(id, socket_name):
    # посылаем сокет с переменными: id-id объекта, socket_name-имя, по которому следует назначать событие в скрипте js
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'wall',
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)
