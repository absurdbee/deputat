from datetime import date
today = date.today()
from common.notify.progs import *

""" Сохранение уведомления о событиях записей. - user_post_notify, community_post_notify
    Мы создаём группы уведомлений по сегодняшнему дню, исключая случаи, когда creator != recipient:
    1. Если пользователь уже делал "тип уведомления", то запись не создается
    2. Фильтруем записи уведомлений постов. Если есть запись, которую создал
        creator, а получатель её recipient, и verb совпадает с verb этой записи, значит создаём новую запись с прикреплением её
        к найденной записи. Это пример уведомлений "Тот-то оценил 2 Ваши записи".
    3. Если записи нет, тогда снова ищем, но только по совпадению "получатель её recipient, id объекта post_id
        и verb совпадает с verb" за сегодняший день. Если запись есть, то создаем новую и прицепляем к ней.
        Это пример уведомлений "Тот-то и тот-то оценили пост" или "Тот-то и ещё 7 человек оценили пост".
    4. Если ни той, ни той записи нет, тогда просто создаем новую запись. Пример уведомлений
        "Тот-то оценил Ваш пост".
"""

def user_notify(creator, action_community_id, object_id, type, socket_name, verb, owner_id):
    from notify.models import Notify

    current_verb = creator.get_verb_gender(verb)
    if Notify.objects.filter(creator_id=creator.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=current_verb).exists():
        return

    if owner_id:
        recipient_ids = creator.get_member_for_notify_ids() + [owner_id]
    else:
        recipient_ids = creator.get_member_for_notify_ids()

    for user_id in recipient_ids:
        if Notify.objects.filter(recipient_id=user_id, action_community_id=action_community_id, created__gt=today, type=type, verb=current_verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, action_community_id=action_community_id, type=type, created__gt=today, verb=current_verb).first()
            Notify.objects.create(creator_id=creator.pk, action_community_id=action_community_id, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb, user_set=notify)
        elif Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
            notify = Notify.objects.get(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb)
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, action_community_id=action_community_id, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, action_community_id=action_community_id, object_id=object_id, type=type, verb=current_verb)
        user_send_notify(object_id, creator.pk, user_id, action_community_id, socket_name)

def community_notify(creator, community, action_community_id, object_id, type, socket_name, verb):
    from notify.models import Notify

    if Notify.objects.filter(creator_id=creator.pk, recipient_id=user_id, community_id=community.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb).exists():
        return

    current_verb = creator.get_verb_gender(verb)
    for user_id in community.get_member_for_notify_ids():
        if Notify.objects.filter(creator_id=creator.pk, recipient_id=user_id, community_id=community.pk, action_community_id=action_community_id, created__gt=today, type=type, verb=verb).exists():
            notify = Notify.objects.get(creator_id=creator.pk, recipient_id=user_id, community_id=community.pk, created__gt=today, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb)
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, community_id=community.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb, user_set=notify)
        elif Notify.objects.filter(community_id=community.pk, recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
            notify = Notify.objects.get(community_id=community.pk, recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb)
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, action_community_id=action_community_id, community_id=community.pk, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, action_community_id=action_community_id, community_id=community.pk, object_id=object_id, type=type, verb=current_verb)
        community_send_notify(object_id, creator.pk, user_id, community, action_community_id, socket_name)


def user_wall(creator, action_community_id, object_id, type, socket_name, verb):
    from notify.models import Wall

    current_verb = creator.get_verb_gender(verb)

    if Wall.objects.filter(creator_id=creator.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb).exists():
        return
    #elif Wall.objects.filter(action_community_id=action_community_id, created__gt=today, object_id, verb=current_verb).exists():
    #    notify = Wall.objects.get(action_community_id=action_community_id, object_id, created__gt=today, verb=current_verb)
    #    Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=current_verb, user_set=notify)
    elif Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).exists():
        notify = Wall.objects.get(object_id=object_id, type=type, created__gt=today, verb=verb)
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
    else:
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=current_verb)
    user_send_wall(object_id, action_community_id, socket_name)

def community_wall(creator, community, action_community_id, object_id, type, socket_name, verb):
    from notify.models import Wall

    current_verb = creator.get_verb_gender(verb)

    if Wall.objects.filter(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb).exists():
        return
    #elif Wall.objects.filter(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, created__gt=today, object_id=object_id, verb=verb).exists():
    #    notify = Wall.objects.get(creator_id=creator.pk, community_id=community.pk, created__gt=today, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb)
    #    Wall.objects.create(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, object_id=object_id, type=type, verb=verb, user_set=notify)
    elif Wall.objects.filter(community_id=community.pk, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
        notify = Wall.objects.get(community_id=community.pk, object_id=object_id, type=type, created__gt=today, verb=verb)
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, community_id=community.pk, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
    else:
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, community_id=community.pk, object_id=object_id, type=type, verb=current_verb)
    community_send_wall(object_id, creator.pk, community, action_community_id, socket_name)


def user_comment_notify(creator, object_id, type, socket_name, verb, owner_id):
    from notify.models import Notify

    if owner_id:
        recipient_ids = creator.get_member_for_notify_ids() + [owner_id]
    else:
        recipient_ids = creator.get_member_for_notify_ids()

    current_verb = creator.get_verb_gender(verb)
    for user_id in recipient_ids:
        if Notify.objects.filter(recipient_id=user_id, created__gt=today, type=type, verb=current_verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, type=type, created__gt=today, verb=current_verb).last()
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb, user_set=notify)
        elif Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, object_id=object_id, type=type, created__gt=today, verb=verb).last()
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb)
        user_send_notify(object_id, creator.pk, user_id, None, socket_name)

def user_comment_wall(creator, object_id, type, socket_name, verb):
    from notify.models import Wall

    current_verb = creator.get_verb_gender(verb)
    if Wall.objects.filter(created__gt=today, type=type, verb=current_verb).exists():
        notify = Wall.objects.filter(type=type, created__gt=today, verb=current_verb).last()
        wall = Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb=current_verb, user_set=notify)
    elif Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).exists():
        notify = Wall.objects.filter(object_id=object_id, type=type, created__gt=today, verb=verb).last()
        wall = Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
    else:
        wall = Wall.objects.create(creator_id=creator.pk, object_id=object_id, type=type, verb=current_verb)
    user_send_wall(object_id, None, socket_name)


def community_comment_notify(creator, community, action_community_id, object_id, type, socket_name, verb):
    from notify.models import Notify
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()
    for user_id in community.get_member_for_notify_ids():
        if Notify.objects.filter(recipient_id=user_id, community_id=community.pk, created__gt=today, type=type, verb=current_verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, community_id=community.pk, type=type, created__gt=today, verb=current_verb).last()
            Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb, user_set=notify)
        elif Notify.objects.filter(recipient_id=user_id, community_id=community.pk, object_id=object_id, type=type, created__gt=today, verb=verb).exists():
            notify = Notify.objects.filter(recipient_id=user_id, community_id=community.pk, object_id=object_id, type=type, created__gt=today, verb=verb).last()
            Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
        else:
            Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, object_id=object_id, type=type, verb=current_verb)
            community_send_notify(object_id, creator.pk, user_id, community.pk, action_community_id, socket_name)

def community_comment_wall(creator, community, object_id, type, socket_name, verb):
    from notify.models import Wall
    from datetime import date

    current_verb, today = creator.get_verb_gender(verb), date.today()
    if Wall.objects.filter(created__gt=today, community_id=community.pk, type=type, verb=current_verb).exists():
        notify = Wall.objects.filter(type=type, community_id=community.pk, created__gt=today, verb=current_verb).last()
        wall = Wall.objects.create(creator_id=creator.pk, community_id=community.pk, object_id=object_id, type=type, verb=current_verb, user_set=notify)
    elif Wall.objects.filter(object_id=object_id, community_id=community.pk, type=type, created__gt=today, verb=verb).exists():
        notify = Wall.objects.filter(object_id=object_id, community_id=community.pk, type=type, created__gt=today, verb=verb).last()
        wall = Wall.objects.create(creator_id=creator.pk, community_id=community.pk, object_id=object_id, type=type, verb="G"+verb, object_set=notify)
    else:
        wall = Wall.objects.create(creator_id=creator.pk, community_id=community.pk, object_id=object_id, type=type, verb=current_verb)
    community_send_wall(object_id, creator.pk, community.pk, None, socket_name)
