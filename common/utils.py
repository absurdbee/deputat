import json, requests
from users.model.profile import IPUser, UserLocation
import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.shortcuts import render


def try_except(value):
    try:
        if value:
            return True
    except:
        return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(request, user):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    IPUser.objects.create(user=user, ip=ip)
    response = requests.get(url= "http://api.sypexgeo.net/c9Hu3/json/" + ip)
    data = response.json()
    loc = UserLocation.objects.create(user=user)
    sity = data['city']
    region = data['region']
    country = data['country']
    loc.city_ru = sity['name_ru']
    loc.city_en = sity['name_en']
    loc.city_lat = sity['lat']
    loc.city_lon = sity['lon']
    loc.region_ru = region['name_ru']
    loc.region_en = region['name_en']
    loc.country_ru = country['name_ru']
    loc.country_en = country['name_en']
    loc.phone = country['phone']
    loc.save()


def render_for_platform(request, template, data):
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return render(request, template, data)
    else:
        return render(request, template, data)


def get_full_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "generic/phone_verification.html"
        elif request_user.is_suspended():
            template_name = "generic/you_suspended.html"
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
        elif request_user.is_suspended():
            template_name = "generic/you_suspended.html"
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
