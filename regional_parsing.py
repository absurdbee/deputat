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

from city.models import City
from district.models import District
from lists.models import Fraction, AuthorityList


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html, city, district):
    soup = BeautifulSoup(html, 'lxml')

    total_self, total_er, total_ldpr, total_kprf, total_sr, total_place = "", "", "", "", "", ""
    name = soup.find('h1', class_='page-content__headline h1').text

    comparison = soup.find('div', class_='comparison')
    total_voters = comparison.find_all('b', class_='num-el')[0].text

    chapter__sections = soup.find_all('div', class_='chapter__section')

    ratio_table = chapter__sections[0].find('table', class_='ratio-table')
    ratio_tds = ratio_table.find_all('td')
    ratio_tds_count = 0
    for td in ratio_tds:
        p_text = ratio_tds[ratio_tds_count].find('p', class_="ratio-table__label").text
        if p_text == "Самовыдвижение":
            total_self = ratio_tds[ratio_tds_count].find('span').text
        elif p_text == "Единая Россия":
            total_er = ratio_tds[ratio_tds_count].find('span').text
        elif p_text == "ЛДПР":
            total_ldpr = ratio_tds[ratio_tds_count].find('span').text
        elif p_text == "КПРФ":
            total_kprf = ratio_tds[ratio_tds_count].find('span').text
        elif p_text == "Справедливая Россия":
            total_sr = ratio_tds[ratio_tds_count].find('span').text
        ratio_tds_count += 1

    if chapter__sections[0].find('div', class_='summary summary_candidates pb-md-5 pt-3 mb-3 mb-md-1'):
        summary = chapter__sections[0].find_all('div', class_="summary__item")
        if "%" in summary[0].find('b').text:
            man_procent = summary[0].find('b').text
        else:
            total_place = summary[0].find('b').text
            man_procent = summary[1].find('b').text
        chapter_section_3 = chapter__sections[1]
    else:
        chapter_section_2 = chapter__sections[1]
        chapter_section_3 = chapter__sections[2]
        summary = chapter_section_2.find_all('div', class_="summary__item")
        if "%" in summary[0].find('b').text:
            man_procent = summary[0].find('b').text
        else:
            total_place = summary[0].find('b').text
            man_procent = summary[1].find('b').text

    if city:
        city.name = name
        city.total_voters = total_voters
        city.total_place = total_place
        city.man_procent = man_procent
        city.total_self = total_self
        city.total_er = total_er
        city.total_ldpr = total_ldpr
        city.total_sr = total_sr
        city.total_kprf = total_kprf
        city.save()
        print("Город заполнен ", city.name)
    elif district:
        district.name = name
        district.total_voters = total_voters
        district.total_place = total_place
        district.man_procent = man_procent
        district.total_self = total_self
        district.total_er = total_er
        district.total_ldpr = total_ldpr
        district.total_sr = total_sr
        district.total_kprf = total_kprf
        district.save()
        print("Район заполнен ", district.name)

    _list = AuthorityList.objects.get(name="Кандидат")

    deputats_body = chapter_section_3.find('tbody')
    deputat_items = deputats_body.find_all('tr')

    for item in deputat_items:
        person = item.find('div', class_="person-item person-item_row js-popup-trigger")
        person_span = person.find_all('span')

        _name = person_span[0].text
        try:
            _fraction = Fraction.objects.get(name=person_span[1].text)
        except:
            _fraction = Fraction.objects.get(name="Без фракции")
        _post = item.find_all('p', class_="js-foldable")[0].text
        old = item.find_all('td', class_="is-hidden-mobile")[0].text

        is_elect_exists = False
        try:
            elects = Elect.objects.filter(name=_name)
            for i in elects:
                if i.calculate_age() == old:
                    is_elect_exists = True
        except:
            pass

        if not is_elect_exists:
            elect = Elect.objects.create(name=_name, birthday=old, post=_post, fraction=_fraction)
            elect.list.add(_list)
            if city:
                elect.city.add(city)
            elif district:
                elect.district.add(district)
            print("Добавлен кандидат ", elect.name)

def main():
    for city in City.objects.all():
        print("работаю с городом ", city.name)
        html = get_html("https://election.novayagazeta.ru/region/" + city.link + "/")
        get_page_data(html, city, None)
        break
    for district in District.objects.all():
        html = get_html("https://election.novayagazeta.ru/region/" + district.link + "/")
        get_page_data(html, None, district)

if __name__ == '__main__':
    main()
