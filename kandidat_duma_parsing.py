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
from okrug.models import Okrug


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html, region):
    soup = BeautifulSoup(html, 'lxml')

    h5_list = soup.find_all('h5')
    h5_count = 0

    _list = AuthorityList.objects.get(slug="candidate_duma")

    tgrids = soup.find_all('div', class_='tgrid')
    parth = 0
    for tgrid in tgrids:
        #if not Okrug.objects.filter(name=h5_list[h5_count].text, region=region).exists():
        #    okrug = Okrug.objects.create(name=h5_list[h5_count].text, region=region)
        #else:
        #    okrug = Okrug.objects.get(name=h5_list[h5_count].text, region=region)

        h5_count = h5_count + 2

        deputat_items = tgrid.find_all('div', class_='trow')
        count = 0
        parth += 1

        for item in deputat_items:
            if not count == 0:
                name = item.find("b").text
                patr = item.find('p', class_='party-name').text
                if patr == "ЕДИНАЯ РОССИЯ":
                    _patr = Fraction.objects.get(name="Единая Россия")
                elif patr == "ЛДПР":
                    _patr = Fraction.objects.get(name="ЛДПР")
                elif patr == "КПРФ":
                    _patr = Fraction.objects.get(name="КПРФ")
                elif patr == "СПРАВЕДЛИВАЯ РОССИЯ - ЗА ПРАВДУ":
                    _patr = Fraction.objects.get(name="Справедливая Россия")
                elif patr == "Гражданская Платформа":
                    _patr = Fraction.objects.get(name="Гражданская Платформа")
                elif patr == "ЗЕЛЕНАЯ АЛЬТЕРНАТИВА":
                    _patr = Fraction.objects.get(name="Зеленая Альтернатива")
                elif patr == "Зеленые":
                    _patr = Fraction.objects.get(name="Зеленые")
                elif patr == "КОММУНИСТЫ РОССИИ":
                    _patr = Fraction.objects.get(name="Коммунисты России")
                elif patr == "НОВЫЕ ЛЮДИ":
                    _patr = Fraction.objects.get(name="Новые люди")
                elif patr == "Партия пенсионеров":
                    _patr = Fraction.objects.get(name="Партия пенсионеров")
                elif patr == "ПАРТИЯ РОСТА":
                    _patr = Fraction.objects.get(name="Партия роста")
                elif patr == "РПСС":
                    _patr = Fraction.objects.get(name="РПСС")
                elif patr == "РОДИНА":
                    _patr = Fraction.objects.get(name="Родина")
                elif patr == "ЯБЛОКО":
                    _patr = Fraction.objects.get(name="Яблоко")
                else:
                    _patr = Fraction.objects.get(slug="no_fraction")

                #deps = item.find_all('li')
                #if "Возраст" in deps[0].text:
                #    _birthday=deps[0].text.replace("Возраст: ","")
                #else:
                #    _birthday=deps[1].text.replace("Возраст: ","")
                #if "Образование" in deps[2].text:
                #    _description=deps[2].text.replace("Образование: ","")
                #elif "Образование" in deps[1].text:
                #    _description=deps[1].text.replace("Образование: ","")
                #else:
                #    _description=""

                #if not Elect.objects.filter(name=name, region=region, okrug=okrug).exists():
                #    elect = Elect.objects.create(
                #                    name=name,
                #                    okrug=okrug,
                #                    post_2=item.find("p", class_='fio').text.replace(name + ", ",""),
                #                    birthday=_birthday,
                #                    description=_description,
                #                    fraction=_patr
                #                )
                #    if item.find("img")["src"] == "/wp-content/uploads/imagefb.jpg":
                #        img = 'https://xn--80aietlhndtbf.xn--p1acf/static/images/elect_image.png'
                #    else:
                #        img = "https://gosduma-2021.com/" + item.find("img")["src"]
                #    try:
                #        elect.get_remote_image(img)
                #    except:
                #        pass
                #    elect.region.add(region)
                #    elect.list.add(_list)
                #    print(elect.name, " добавлен!")
                #else:
                try:
                    elect = Elect.objects.get(name=name, region=region,list=_list)
                    elect.fraction = _patr
                    elect.save(update_fields=["fraction"])
                    print("Фракция обновлена")
                except:
                    print("Что то не так!")
            count += 1
            print("--------------------")
        print("=======================")

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
