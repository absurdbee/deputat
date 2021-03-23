from django.db.models import Q
from notify.models import Notify


def get_news(user):
    query = Q(user_set__isnull=True, object_set__isnull=True)
    return Notify.objects.filter(query)

def get_my_news(user):
    query = Q(creator_id__in=user.get_user_news_notify_ids())|\
            Q(creator_id__in=user.get_user_profile_notify_ids())
    query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
    return Notify.objects.filter(query)

def get_draft_news(user):
    query = Q(verb="SIT") & Q(user_set__isnull=True, object_set__isnull=True)
    return Notify.objects.filter(query)

def user_notify(creator, recipient_id, attach, socket_name, verb):
    from notify.models import Notify
    from datetime import date
    today = date.today()

    current_verb = creator.get_verb_gender(verb)

    if Notify.objects.filter(creator_id=creator.pk, recipient_id=recipient_id, attach=attach, verb=verb).exists():
        pass
    elif Notify.objects.filter(recipient_id=recipient_id, created__gt=today, attach__contains=attach[:3], verb=current_verb).exists():
        notify = Notify.objects.get(recipient_id=recipient_id, attach__contains=attach[:3], created__gt=today, verb=current_verb)
        Notify.objects.create(creator_id=creator.pk, recipient_id=recipient_id, attach=attach, verb=current_verb, user_set=notify)
    elif Notify.objects.filter(recipient_id=recipient_id, attach=attach, created__gt=today, verb=verb).exists():
        notify = Notify.objects.get(recipient_id=recipient_id, attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator_id=creator.pk, recipient_id=recipient_id, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Notify.objects.create(creator_id=creator.pk, recipient_id=recipient_id, attach=attach, verb=current_verb)
    #user_send(attach[3:], recipient_id, socket_name)


def get_notify(user, notify):
    attach = notify.attach
    if attach[:3] == "blo":
        from common.items.blog import get_blog
        if notify.verb == "ITE":
            return get_blog(user, attach[3:])
        else:
            if notify.is_have_user_set():
                first_notify = notify.get_first_user_set()
                return '<p style="padding: 10px 20px;"><a href="/users/' + str(first_notify.creator.pk) + '" class="ajax">' + first_notify.creator.get_full_name() + '</a> '\
                + first_notify.get_verb_display() + ' ' + str(notify.count_user_set()) + '</p>'
            elif notify.is_have_object_set():
                first_notify = notify.get_first_object_set()
                return '<p style="padding-left: 7px;"><a href="/users/' + str(first_notify.creator.pk) + '" class="ajax" style="font-weight: bold;">'+ \
                first_notify.creator.get_full_name() + '</a> и ещё ' + str(notify.count_object_set()) + first_notify.get_verb_display()\
                 + ' новость проекта </p>' + get_blog(user, attach[3:])
            else:
                return '<p style="padding-left: 7px;"><a href="/users/' + str(notify.creator.pk) + '" class="ajax" style="font-weight: bold;">'+ \
                notify.creator.get_full_name() + '</a>' + notify.get_verb_display()\
                 + ' новость проекта </p>' + get_blog(user, attach[3:])
