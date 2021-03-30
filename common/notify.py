from django.db.models import Q
from notify.models import Notify, Wall


def get_news():
    # пока исключаем из выдачи группировку "оценил три поста" user_set__isnull=True
    query = Q(object_set__isnull=True)
    return Notify.objects.filter(query)

def get_region_news(name):
    # пока исключаем из выдачи группировку "оценил три поста" user_set__isnull=True
    query = Q(object_set__isnull=True) & Q(options__icontains=name)
    return Notify.objects.filter(query)


def get_my_news(user):
    query = Q(creator_id__in=user.get_user_news_notify_ids())|\
            Q(creator_id__in=user.get_user_profile_notify_ids())
    query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
    return Notify.objects.filter(query)

def get_draft_news(user):
    query = Q(verb="SIT") & Q(user_set__isnull=True, object_set__isnull=True)
    return Notify.objects.filter(query)

def user_notify(creator, attach, socket_name, verb):
    from notify.models import Notify
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()
    for user_id in creator.get_member_for_notify_ids():
        if Notify.objects.filter(creator_id=creator.pk, recipient_id=user_id, attach=attach, verb=verb).exists():
            pass
        elif Notify.objects.filter(recipient_id=user_id, created__gt=today, attach__contains=attach[:3], verb=current_verb).exists():
            notify = Notify.objects.get(recipient_id=user_id, attach__contains=attach[:3], created__gt=today, verb=current_verb)
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach=attach, verb=current_verb, user_set=notify)
        elif Notify.objects.filter(recipient_id=user_id, attach=attach, created__gt=today, verb=verb).exists():
            notify = Notify.objects.get(recipient_id=user_id, attach=attach, created__gt=today, verb=verb)
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach=attach, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach=attach, verb=current_verb)
            send_notify_socket(attach[3:], user_id, socket_name)

def user_wall(creator, attach, socket_name, verb):
    from notify.models import Wall
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()

    if Notify.objects.filter(creator_id=creator.pk, attach=attach, verb=verb).exists():
        pass
    #elif Notify.objects.filter(created__gt=today, attach__contains=attach[:3], verb=current_verb).exists():
    #    notify = Notify.objects.get(attach__contains=attach[:3], created__gt=today, verb=current_verb)
    #    Notify.objects.create(creator_id=creator.pk, attach=attach, verb=current_verb, user_set=notify)
    elif Notify.objects.filter(attach=attach, created__gt=today, verb=verb).exists():
        notify = Notify.objects.get(attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator_id=creator.pk, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Notify.objects.create(creator_id=creator.pk, attach=attach, verb=current_verb)
    send_wall_socket(attach[3:], socket_name)


def get_notify(user, notify):
    attach = notify.attach
    if attach[:3] == "blo":
        from common.items.blog import get_blog
        if notify.verb == "ITE":
            return get_blog(user, attach[3:])
        else:
            if notify.is_have_user_set():
                first_notify = notify.get_first_user_set()
                return '<p style="padding: 10px 20px;"><a href="/users/' + str(first_notify.creator.pk) + '/" class="ajax">' + first_notify.creator.get_full_name() + '</a> '\
                + first_notify.get_verb_display() + ' ' + str(notify.count_user_set()) + '</p>'
            if notify.is_have_object_set():
                first_notify = notify.get_first_object_set()
                return '<p style="padding-left: 7px;"><a href="/users/' + str(first_notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">'+ \
                first_notify.creator.get_full_name() + '</a> и ещё ' + str(notify.count_object_set()) + first_notify.get_verb_display()\
                 + ' новость проекта </p>' + get_blog(user, attach[3:])
            else:
                return '<p style="padding-left: 7px;"><a href="/users/' + str(notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">'+ \
                notify.creator.get_full_name() + '</a>' + notify.get_verb_display()\
                 + ' новость проекта </p>' + get_blog(user, attach[3:])


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
        'name': "u_post_create",
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def send_wall_socket(id, socket_name):
    # посылаем сокет с переменными: id-id объекта, socket_name-имя, по которому следует назначать событие в скрипте js
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_laye

    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)
