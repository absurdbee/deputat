from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied

def update_activity(user, user_agent):
    from datetime import datetime
    import re
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(user_agent):
        user.last_activity, user.device = datetime.now(), "Ph"
        user.save(update_fields=['last_activity', 'device'])
    else:
        user.last_activity, user.device = datetime.now(), "De"
        user.save(update_fields=['last_activity', 'device'])

def get_folder(user_agent):
    import re
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(user_agent):
        return ""
    else:
        return ""

"""
    кончаются на item - шаблоны для списков и элементов в полную страницу
    кончаются на window - шаблоны для списков и элементов в открывающемся окне,
    в этом случае при проблемных случаях возвращаем таблицу "Ощибка доступа".
"""

def get_fine_request_user(request_user):
    if request_user.is_no_phone_verified():
        return "main/phone_verification.html"
    elif request_user.is_deleted():
        return "generic/u_template/you_deleted.html"
    elif request_user.is_closed():
        return "generic/u_template/you_closed.html"
    elif request_user.is_suspended():
        return "generic/u_template/you_suspended.html"

def get_fine_community_item(request_user, community, item, folder, template):
    if item.is_deleted():
        if request_user.is_administrator_of_community(community.pk) and item.community.pk == community.pk:
            return folder + "admin_deleted_" + template
        else:
            return "generic/c_template/deleted.html"
    elif item.is_closed():
        if staff:
            return folder + "staff_closed_" + template
        if request_user.is_administrator_of_community(community.pk) and item.community.pk == community.pk:
            return "generic/c_template/admin_closed.html"
        else:
            return "generic/c_template/closed.html"
    elif item.is_suspended():
        if staff:
            return folder + "staff_suspended_" + template
        if request_user.is_administrator_of_community(community.pk) and item.community.pk == community.pk:
            return "generic/c_template/admin_suspended.html"
        else:
            return "generic/c_template/suspended.html"
def get_anon_fine_community_item(community, item):
    if item.is_deleted():
        return "generic/c_template/anon_deleted.html"
    elif item.is_closed():
        return "generic/c_template/anon_closed.html"
    elif item.is_suspended():
        return "generic/c_template/anon_suspended.html"
def get_fine_user_item(request_user, item, folder, template):
    if item.is_deleted():
        if item.creator.pk == request_user.pk:
            return folder + "my_deleted_" + template
        else:
            return "generic/u_template/deleted.html"
    elif item.is_closed():
        if item.creator.pk == request_user.pk:
            return folder + "my_closed_" + template
        else:
            return "generic/u_template/closed.html"
    elif item.is_suspended():
        if item.creator.pk == request_user.pk:
            return folder + "my_suspended_" + template
        else:
            return "generic/u_template/suspended.html"
def get_fine_user(user):
    if user.is_suspended():
        return "generic/u_template/user_suspended.html"
    elif user.is_deleted():
        return "generic/u_template/user_deleted.html"
    elif user.is_closed():
        return "generic/u_template/user_global_block.html"
def get_fine_anon_user(user):
    if user.is_suspended():
        return "generic/u_template/anon_user_suspended.html"
    elif user.is_deleted():
        return "generic/u_template/anon_user_deleted.html"
    elif user.is_closed():
        return "generic/u_template/anon_user_closed.html"
def get_anon_fine_user_list(list):
    if list.is_deleted():
        return "generic/u_template/anon_deleted.html"
    elif list.is_closed():
        return "generic/u_template/anon_closed.html"
    elif list.is_suspended():
        return "generic/u_template/anon_suspended.html"


def get_detect_platform_template(template, request_user, user_agent):
    """ получаем шаблон для зарегистрированного пользователя. Анонимов не пускаем."""
    if request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    elif request_user.type[0] == "_":
        template = get_fine_request_user(request_user)
    else:
        template = template
    update_activity(request_user, user_agent)
    return get_folder(user_agent) + template


def render_for_platform(request, template, data):
    import re
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return render(request, template, data)
    else:
        return render(request, template, data)


def get_full_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = template
    elif request_user.is_anonymous:
        template_name = template
    return get_folder(user_agent) + template_name


def get_small_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = template
    elif request_user.is_anonymous:
        template_name = template
    return get_folder(user_agent) + template_name


def get_managers_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        elif request_user.is_manager() or request_user.is_superuser:
            template_name = template
        else:
            raise PermissionDenied("Permission denied...")
    else:
        raise PermissionDenied("Permission denied...")
    return get_folder(user_agent) + template_name

def get_my_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = template
    else:
        raise PermissionDenied("Permission denied...")
    return get_folder(user_agent) + template_name

def get_template_community_item(item, folder, template, request_user, user_agent, staff):
    # Полная страница объекта сообщества (списка или элемента) для зарегистрированного пользователя
    community = item.community
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif community.type[0] == "_":
        template_name = get_fine_community(request_user, community)
    elif item.type[0] == "_":
        template_name = get_fine_community_item(request_user, community, item, folder, template)
    elif request_user.is_member_of_community(community.pk):
        if request_user.is_administrator_of_community(community.pk):
            template_name = folder + "admin_" + template
        elif staff:
            template_name = folder + "staff_member_" + template
        elif item.is_private():
            template_name = "generic/c_template/private.html"
        else:
            template_name = folder + "member_" + template
    elif staff:
        template_name = folder + "staff_" + template
    elif community.is_close():
        if request_user.is_follow_from_community(community.pk):
            template_name = "generic/c_template/follow_community.html"
        else:
            template_name = "generic/c_template/close_community.html"
    elif community.is_private():
        template_name = "generic/c_template/private_community.html"
    elif request_user.is_banned_from_community(community.pk):
        template_name = "generic/c_template/block_community.html"
    elif community.is_public():
        if item.is_private():
            template_name = "generic/c_template/private.html"
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_community_item(item, template, user_agent):
    # Полная страница объекта сообщества (списка или элемента) для анонимного пользователя
    community = item.community
    if community.type[0] == "_":
        template_name = get_anon_fine_community(community)
    elif item.type[0] == "_":
        template_name  = get_anon_fine_community(community, item)
    elif community.is_public():
        if not community.is_verified():
            template_name = "generic/c_template/anon_no_child_safety.html"
        elif item.is_private():
            template_name = "generic/c_template/anon_private.html"
        else:
            template_name = template
    elif community.is_close():
        template_name = "generic/c_template/anon_close_community.html"
    elif community.is_private():
        template_name = "generic/c_template/anon_private_community.html"
    return get_folder(user_agent) + template_name

def get_template_user_item(item, folder, template, request_user, user_agent, staff):
    # Полная страница объекта пользователя (списка или элемента) для зарегистрированного пользователя
    user = item.creator
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif item.type[0] == "_":
        template_name = get_fine_user_item(request_user, item, folder, template)
    elif user.pk == request_user.pk:
            template_name = folder + "my_" + template
    elif request_user.pk != user.pk:
        if user.type[0] == "_":
            template_name = get_fine_user(user)
        elif staff or request_user.is_superuser:
            template_name = folder + "staff_" + template
        elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
            template_name = "generic/u_template/block_user.html"
        elif item.is_private():
            template_name = "generic/u_template/private.html"
        else:
            template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_user_item(item, template, user_agent):
    # Полная страница объекта сообщества (списка или элемента) для анонимного пользователя
    user = item.creator
    if user.type[0] == "_":
        template_name = get_fine_user(user)
    elif item.type[0] == "_":
        template_name = get_anon_fine_user_item(item)
    elif not user.is_child_safety():
        template_name = "generic/u_template/anon_no_child_safety.html"
    elif item.is_private():
        template_name = "generic/u_template/anon_private.html"
    else:
        template_name = template
    return get_folder(user_agent) + template_name


def get_template_community_window(item, folder, template, request_user, user_agent, staff):
    # Полная страница объекта сообщества (списка или элемента) для зарегистрированного пользователя
    community = item.community
    if request_user.type[0] == "_" or community.type[0] == "_" or item.type[0] == "_":
        template_name = "generic/c_template/permission_window.html"
    elif request_user.is_member_of_community(community.pk):
        if request_user.is_administrator_of_community(community.pk):
            template_name = folder + "admin_" + template
        elif staff:
            template_name = folder + "staff_member_" + template
        elif item.is_private():
            template_name = "generic/c_template/permission_window.html"
        else:
            template_name = folder + "member_" + template
    elif staff:
        template_name = folder + "staff_" + template
    elif community.is_close() or community.is_private() or request_user.is_banned_from_community(community.pk):
        template_name = "generic/c_template/permission_window.html"
    elif community.is_public():
        if item.is_private():
            template_name = "generic/c_template/permission_window.html"
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_community_window(item, template, user_agent):
    # Полная страница объекта сообщества (списка или элемента) для анонимного пользователя
    community = item.community
    if community.type[0] == "_" or item.type[0] == "_" or community.is_close() or community.is_private() or item.is_private():
        template_name = "generic/c_template/permission_window.html"
    else:
        template_name = template
    return get_folder(user_agent) + template_name

def get_template_user_window(item, folder, template, request_user, user_agent, staff):
    # Полная страница объекта пользователя (списка или элемента) для зарегистрированного пользователя
    user = item.creator
    if request_user.type[0] == "_" or item.type[0] == "_" or user.type[0] == "_":
        template_name = "generic/u_template/permission_window.html"
    elif user.pk == request_user.pk:
            template_name = folder + "my_" + template
    elif request_user.pk != user.pk:
        if staff or request_user.is_superuser:
            template_name = folder + "staff_" + template
        elif request_user.is_blocked_with_user_with_id(user_id=user.pk) and item.is_private():
            template_name = "generic/u_template/permission_window.html"
        else:
            template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_user_window(item, template, user_agent):
    # Полная страница объекта сообщества (списка или элемента) для анонимного пользователя
    user = item.creator
    if user.type[0] == "_" or item.type[0] == "_" or item.is_private():
        template_name = "generic/u_template/permission_window.html"
    else:
        template_name = template
    return get_folder(user_agent) + template_name
