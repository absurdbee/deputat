from django.db.models import Q
from notify.models import Notify


def get_news(user):
    """ лента всех новостей - первая вкладка на главной странице

        Примечания:
        - список покажет все уведомления по времени. Вложения уведомлений создаются на срок одного дня.
        - прикрепленные элементы просто записаны в текстовое поле, например pho_19 - это фотка под номером 19. Так
            пользователь увидит все действия, как и в контакте.
    """
    query = Q(user_set__isnull=True, object_set__isnull=True)
    return Notify.objects.filter(query)

def get_subscribes_news(user):
    """ лента новостей, куда попадают все взаимодействия людей: - вторая вкладка
        1. Активности, комментарии, лайки/дизлайки, голосования и т.д. тех людей, на которых человек подписан
        2. Учитываются прямые подписки людей (get_user_news_notify_ids),
            а также созданные по нажатию на колокольчик (get_user_profile_notify_ids)

        Примечания:
        - список покажет все уведомления по времени. Вложения уведомлений создаются на срок одного дня.
        - прикрепленные элементы просто записаны в текстовое поле, например pho_19 - это фотка под номером 19. Так
            пользователь увидит все действия, как и в контакте.
    """
    query = Q(creator_id__in=user.get_user_news_notify_ids())|\
            Q(creator_id__in=user.get_user_profile_notify_ids())
    query.add(Q(user_set__isnull=True, object_set__isnull=True), Q.AND)
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
