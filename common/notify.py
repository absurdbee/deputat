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

def get_notify(user, notify):
    type = notify.type
    if type == "BLO":
        from common.items.blog import get_blog
        return get_blog(user, notify)
    elif type == "BLOC":
        from common.items.blog import get_comment_blog
        return get_comment_blog(user, notify)
