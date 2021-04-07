import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied

def render_for_platform(request, template, data):
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return render(request, template, data)
    else:
        return render(request, template, data)


def get_full_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "generic/phone_verification.html"
        elif request_user.is_blocked():
            template_name = "generic/you_global_block.html"
        elif request_user.is_manager():
            template_name = template
        else:
            template_name = template
    elif request_user.is_anonymous:
        template_name = template
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = template_name
    else:
        template_name = template_name
    return template_name


def get_small_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "generic/phone_verification.html"
        elif request_user.is_blocked():
            template_name = "generic/you_global_block.html"
        else:
            template_name = template
    elif request_user.is_anonymous:
        template_name = template
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = template_name
    else:
        template_name = template_name
    return template_name


def get_managers_template(template, request_user, user_agent):
    if request_user.is_authenticated and (request_user.is_manager() or request_user.is_superuser):
        template_name = template
    else:
        raise PermissionDenied("Permission denied...")
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = template_name
    else:
        template_name = template_name
    return template_name

def get_my_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        template_name = template
    else:
        raise PermissionDenied("Permission denied...")
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = template_name
    else:
        template_name = template_name
    return template_name

def get_list_template(list, folder, template, request_user, user_agent):
    user = list.creator
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "generic/phone_verification.html"
        elif user.pk == request_user.pk:
            if user.is_suspended():
                template_name = "generic/you_suspended.html"
            elif user.is_blocked():
                template_name = "generic/you_global_block.html"
            else:
                template_name = folder + "my_" + template
        elif request_user.pk != user.pk:
            if user.is_suspended():
                template_name = "generic/user_suspended.html"
            elif user.is_blocked():
                template_name = "generic/user_global_block.html"
            elif request_user.is_manager() or request_user.is_supermanager():
                template_name = folder + "staff_" + template
            elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
                template_name = "generic/u_template/you_block_from_user.html"
            elif list.type == "PRI":
                template_name = folder + "private_" + template
            else:
                template_name = folder + template
    elif request_user.is_anonymous:
        if user.is_suspended():
            template_name = "generic/anon_user_suspended.html"
        elif user.is_blocked():
            template_name = "generic/anon_user_global_block.html"
        elif list.type == "PRI":
            template_name = folder + "anon_private_" + template
        else:
            template_name = folder + "anon_" + template
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = template_name
    else:
        template_name = template_name
    return template_name

def get_item_template(item, folder, template, request_user, user_agent):
    user = item.creator
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "generic/phone_verification.html"
        elif user.pk == request_user.pk:
            if user.is_suspended():
                template_name = "generic/you_suspended.html"
            elif user.is_blocked():
                template_name = "generic/you_global_block.html"
            else:
                template_name = folder + "my_" + template
        elif request_user.pk != user.pk:
            if user.is_suspended():
                template_name = "generic/user_suspended.html"
            elif user.is_blocked():
                template_name = "generic/user_global_block.html"
            elif request_user.is_manager() or request_user.is_supermanager():
                template_name = folder + "staff_" + template
            elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
                template_name = "generic/u_template/you_block_акщь_user.html"
            elif item.type == "PRI":
                template_name = folder + "private_" + template
            else:
                template_name = folder + template
    elif request_user.is_anonymous:
        if user.is_suspended():
            template_name = "generic/anon_user_suspended.html"
        elif user.is_blocked():
            template_name = "generic/anon_user_global_block.html"
        elif item.type == "PRI":
            template_name = folder + "anon_private_" + template
        else:
            template_name = folder + "anon_" + template
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = template_name
    else:
        template_name = template_name
    return template_name
