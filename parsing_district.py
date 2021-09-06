import sys,os
import re
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()


from region.models import Region
from district.models import District2

spb_oblast_list = [
                    "Бокситогорский муниципальный район",
                    "Волосовский муниципальный район",
                    "Волховский муниципальный район",
                    "Всеволожский муниципальный район",
                    "Выборгский муниципальный район",
                    "Гатчинский муниципальный район",
                    "Кингисеппский муниципальный район",
                    "Киришский муниципальный район",
                    "Кировский муниципальный район",
                    "Лодейнопольский муниципальный район",
                    "Ломоносовский муниципальный район",
                    "Лужский муниципальный район",
                    "Подпорожский муниципальный район",
                    "Приозерский муниципальный район",
                    "Сланцевский муниципальный район",
                    "Сосновоборский городской округ",
                    "Тихвинский муниципальный район",
                    "Тосненский муниципальный район"
                    ]


region = Region.objects.get(name="Ленинградская область")
for i in spb_oblast_list:
    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + i)
    data = response.json()
    count = 0
    for i in data:
        d = District2.objects.create(name=i, region=region, link=data[count][2])
        count += 1
        print ("Добавлен дистрикт ", d.name)
    print ("==============================")
