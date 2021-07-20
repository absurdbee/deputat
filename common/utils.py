import json, requests
from users.model.profile import IPUser, UserLocation


def check_manager_state(user):
    if not user.is_user_manager() or not user.is_community_manager() or not user.is_elect_new_manager() or not user.is_blog_manager() \
        or not user.is_photo_manager() or not user.is_survey_manager() or not user.is_audio_manager() or not user.is_video_manager():
        user.type = 'STA'
        user.save(update_fields=['type'])

def check_supermanager_state(user):
    if not user.is_community_supermanager() or not user.is_elect_new_supermanager() or not user.is_blog_supermanager() \
        or not user.is_good_supermanager() or not user.is_photo_supermanager() or not user.is_audio_supermanager() \
        or not user.is_survey_manager() or not user.is_video_supermanager():
        user.type = 'STA'
        user.save(update_fields=['type'])


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
    response = requests.get(url= "http://api.sypexgeo.net/CeaX9/json/" + ip) 
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
