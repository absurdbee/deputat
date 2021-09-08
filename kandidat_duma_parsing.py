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
from lists.models import Fraction, AuthorityList
from elect.models import Elect


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html, district):
    soup = BeautifulSoup(html, 'lxml')

    _list = AuthorityList.objects.get(name="Кандидат в депутаты гос. думы")

    tgrids = soup.find_all('div', class_='tgrid')
    deputat_items = tgrids.find_all('div', class_='trow')
    count = 0

    for item in deputat_items:
        if count = 0:
            pass
        person = item.find('div', class_="person-item person-item_row js-popup-trigger")
        person_span = person.find_all('span')

        _name = person_span[0].text
        try:
            _fraction = Fraction.objects.get(name=person_span[1].text)
        except:
            _fraction = Fraction.objects.get(name="Без фракции")
        _post = item.find_all('p', class_="js-foldable")[0].text
        old = item.find_all('td', class_="is-hidden-mobile")[0].text
        if not Elect.objects.filter(name=_name, area=district).exists():
            elect = Elect.objects.create(name=_name, birthday=old, post_2=_post[:390], fraction=_fraction)
            elect.list.add(_list)
            elect.area.add(district)
            print("Добавлен кандидат ", elect.name)
        count += 1

def main():
    for region in Region.objects.all():
        if region.name == "Алтайский край":
            html = get_html("https://gosduma-2021.com/s/altaiskii-krai/")
            get_page_data(html, region)
        elif region.name == "Амурская область":
            html = get_html("https://gosduma-2021.com/s/amurskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Архангельская область":
            html = get_html("https://gosduma-2021.com/s/arhangelskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Астраханская область":
            html = get_html("https://gosduma-2021.com/s/astrahanskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Белгородская область":
            html = get_html("https://gosduma-2021.com/s/belgorodskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Брянская область":
            html = get_html("https://gosduma-2021.com/s/bryanskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Владимирская область":
            html = get_html("https://gosduma-2021.com/s/vladimirskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Волгоградская область":
            html = get_html("https://gosduma-2021.com/s/volgogradskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Вологодская область":
            html = get_html("https://gosduma-2021.com/s/vologodskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Воронежская область":
            html = get_html("https://gosduma-2021.com/s/voronejskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Еврейская автономная область":
            html = get_html("https://gosduma-2021.com/s/evreiskaya-avtonomnaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Забайкальский край":
            html = get_html("https://gosduma-2021.com/s/zabaikalskii-krai/")
            get_page_data(html, region)
        elif region.name == "Ивановская область":
            html = get_html("https://gosduma-2021.com/s/ivanovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Иркутская область":
            html = get_html("https://gosduma-2021.com/s/irkutskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Кабардино-Балкарская Республика":
            html = get_html("https://gosduma-2021.com/s/kabardino-balkarskaya-respublika/")
            get_page_data(html, region)
        elif region.name == "Калининградская область":
            html = get_html("https://gosduma-2021.com/s/kaliningradskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Калужская область":
            html = get_html("https://gosduma-2021.com/s/kalujskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Камчатский край":
            html = get_html("https://gosduma-2021.com/s/kamchatskii-krai/")
            get_page_data(html, region)
        elif region.name == "Карачаево-Черкесская Республика":
            html = get_html("https://gosduma-2021.com/s/karachaevo-cherkesskaya-respublika/")
            get_page_data(html, region)
        elif region.name == "Кемеровская область":
            html = get_html("https://gosduma-2021.com/s/kemerovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Кировская область":
            html = get_html("https://gosduma-2021.com/s/kirovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Костромская область":
            html = get_html("https://gosduma-2021.com/s/kostromskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Краснодарский край":
            html = get_html("https://gosduma-2021.com/s/krasnodarskii-krai/")
            get_page_data(html, region)
        elif region.name == "Красноярский край":
            html = get_html("https://gosduma-2021.com/s/krasnoyarskii-krai/")
            get_page_data(html, region)
        elif region.name == "Курганская область":
            html = get_html("https://gosduma-2021.com/s/kurganskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Курская область":
            html = get_html("https://gosduma-2021.com/s/kurskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Ленинградская область":
            html = get_html("https://gosduma-2021.com/s/leningradskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Липецкая область":
            html = get_html("https://gosduma-2021.com/s/lipeckaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Магаданская область":
            html = get_html("https://gosduma-2021.com/s/magadanskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Москва":
            html = get_html("https://gosduma-2021.com/s/g-moskva/")
            get_page_data(html, region)
        elif region.name == "Московская область":
            html = get_html("https://gosduma-2021.com/s/moskovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Мурманская область":
            html = get_html("https://gosduma-2021.com/s/murmanskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Ненецкий автономный округ":
            html = get_html("https://gosduma-2021.com/s/neneckii-avtonomnyi-okrug/")
            get_page_data(html, region)
        elif region.name == "Нижегородская область":
            html = get_html("https://gosduma-2021.com/s/nijegorodskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Новгородская область":
            html = get_html("https://gosduma-2021.com/s/novgorodskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Новосибирская область":
            html = get_html("https://gosduma-2021.com/s/novosibirskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Омская область":
            html = get_html("https://gosduma-2021.com/s/omskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Оренбургская область":
            html = get_html("https://gosduma-2021.com/s/orenburgskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Орловская область":
            html = get_html("https://gosduma-2021.com/s/orlovskaya-oblast/")
            get_page_data(html, region)

        elif region.name == "Пензенская область":
            html = get_html("https://gosduma-2021.com/s/penzenskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Пермский край":
            html = get_html("https://gosduma-2021.com/s/permskii-krai/")
            get_page_data(html, region)
        elif region.name == "Приморский край":
            html = get_html("https://gosduma-2021.com/s/primorskii-krai/")
            get_page_data(html, region)
        elif region.name == "Псковская область":
            html = get_html("https://gosduma-2021.com/s/pskovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Республика Адыгея":
            html = get_html("https://gosduma-2021.com/s/respublika-adygeya/")
            get_page_data(html, region)
        elif region.name == "Республика Алтай":
            html = get_html("https://gosduma-2021.com/s/respublika-altai/")
            get_page_data(html, region)
        elif region.name == "Республика Башкортостан":
            html = get_html("https://gosduma-2021.com/s/respublika-bashkortostan/")
            get_page_data(html, region)
        elif region.name == "Республика Бурятия":
            html = get_html("https://gosduma-2021.com/s/respublika-buryatiya/")
            get_page_data(html, region)
        elif region.name == "Республика Дагестан":
            html = get_html("https://gosduma-2021.com/s/respublika-dagestan/")
            get_page_data(html, region)
        elif region.name == "Республика Ингушетия":
            html = get_html("https://gosduma-2021.com/s/respublika-ingushetiya/")
            get_page_data(html, region)
        elif region.name == "Республика Калмыкия":
            html = get_html("https://gosduma-2021.com/s/respublika-kalmykiya/")
            get_page_data(html, region)
        elif region.name == "Республика Карелия":
            html = get_html("https://gosduma-2021.com/s/respublika-kareliya/")
            get_page_data(html, region)
        elif region.name == "Республика Коми":
            html = get_html("https://gosduma-2021.com/s/respublika-komi/")
            get_page_data(html, region)
        elif region.name == "Республика Крым":
            html = get_html("https://gosduma-2021.com/s/respublika-krym/")
            get_page_data(html, region)
        elif region.name == "Республика Марий Эл":
            html = get_html("https://gosduma-2021.com/s/respublika-marii-el/")
            get_page_data(html, region)
        elif region.name == "Республика Мордовия":
            html = get_html("https://gosduma-2021.com/s/respublika-mordoviya/")
            get_page_data(html, region)
        elif region.name == "Республика Саха (Якутия)":
            html = get_html("https://gosduma-2021.com/s/respublika-saha-yakutiya/")
            get_page_data(html, region)
        elif region.name == "Республика Северная Осетия - Алания":
            html = get_html("https://gosduma-2021.com/s/respublika-severnaya-osetiya/")
            get_page_data(html, region)
        elif region.name == "Республика Татарстан":
            html = get_html("https://gosduma-2021.com/s/respublika-tatarstan/")
            get_page_data(html, region)
        elif region.name == "Республика Тыва":
            html = get_html("https://gosduma-2021.com/s/respublika-tyva/")
            get_page_data(html, region)
        elif region.name == "Республика Хакасия":
            html = get_html("https://gosduma-2021.com/s/respublika-hakasiya/")
            get_page_data(html, region)
        elif region.name == "Ростовская область":
            html = get_html("https://gosduma-2021.com/s/rostovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Рязанская область":
            html = get_html("https://gosduma-2021.com/s/ryazanskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Самарская область":
            html = get_html("https://gosduma-2021.com/s/samarskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Санкт-Петербург":
            html = get_html("https://gosduma-2021.com/s/g-sankt-peterburg/")
            get_page_data(html, region)
        elif region.name == "Саратовская область":
            html = get_html("https://gosduma-2021.com/s/saratovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Сахалинская область":
            html = get_html("https://gosduma-2021.com/s/sahalinskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Свердловская область":
            html = get_html("https://gosduma-2021.com/s/sverdlovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Севастополь":
            html = get_html("https://gosduma-2021.com/s/g-sevastopol/")
            get_page_data(html, region)
        elif region.name == "Смоленская область":
            html = get_html("https://gosduma-2021.com/s/smolenskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Ставропольский край":
            html = get_html("https://gosduma-2021.com/s/stavropolskii-krai/")
            get_page_data(html, region)
        elif region.name == "Тамбовская область":
            html = get_html("https://gosduma-2021.com/s/tambovskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Тверская область":
            html = get_html("https://gosduma-2021.com/s/tverskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Томская область":
            html = get_html("https://gosduma-2021.com/s/tomskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Тульская область":
            html = get_html("https://gosduma-2021.com/s/tulskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Тюменская область":
            html = get_html("https://gosduma-2021.com/s/tumenskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Удмуртская Республика (Удмуртия)":
            html = get_html("https://gosduma-2021.com/s/udmurtskaya-respublika/")
            get_page_data(html, region)
        elif region.name == "Ульяновская область":
            html = get_html("https://gosduma-2021.com/s/ulyanovskaya-oblast/")
            get_page_data(html, region)

        elif region.name == "Хабаровский край":
            html = get_html("https://gosduma-2021.com/s/habarovskii-krai/")
            get_page_data(html, region)
        elif region.name == "Ханты-Мансийский автономный округ - Югра (Тюменская область)":
            html = get_html("https://gosduma-2021.com/s/hanty-mansiiskii-avtonomnyi-okrug/")
            get_page_data(html, region)
        elif region.name == "Челябинская область":
            html = get_html("https://gosduma-2021.com/s/chelyabinskaya-oblast/")
            get_page_data(html, region)
        elif region.name == "Чеченская Республика":
            html = get_html("https://gosduma-2021.com/s/chechenskaya-respublika/")
            get_page_data(html, region)
        elif region.name == "Чувашская Республика - Чувашия":
            html = get_html("https://gosduma-2021.com/s/chuvashskaya-respublika/")
            get_page_data(html, region)
        elif region.name == "Чукотский автономный округ":
            html = get_html("https://gosduma-2021.com/s/chukotskii-avtonomnyi-okrug/")
            get_page_data(html, region)
        elif region.name == "Ямало-Ненецкий автономный округ":
            html = get_html("https://gosduma-2021.com/s/yamalo-neneckii-avtonomnyi-okrug/")
            get_page_data(html, region)
        elif region.name == "Ярославская область":
            html = get_html("https://gosduma-2021.com/s/yaroslavskaya-oblast/")
            get_page_data(html, region)

if __name__ == '__main__':
    main()
