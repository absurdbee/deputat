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
from lists.models import Fraction

def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    total_self, total_er, total_ldpr, total_kprf, total_sr = None, None, None, None, None

    name = soup.find('h1', class_='page-content__headline h1').text
    print ("Название ТЕ ", name)

    comparison = soup.find('div', class_='comparison')
    comparison_integers = comparison.find_all('b', class_='num-el')[0].text
    total_voters = comparison_integers.relpace("&nbsp;", "")
    print ("Избирателей ", total_voters)

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
    print ("Самовыдвижение ", total_self)
    print ("Единая Россия ", total_er)
    print ("ЛДПР ", total_ldpr)
    print ("КПРФ ", total_kprf)
    print ("Справедливая Россия ", total_sr)

    chapter_section_2 = chapter__sections[1]
    summary = chapter_section_2.find_all('div', class_="summary__item")
    total_place = summary[0].find('b').text
    print ("Всего мест ", total_place)
    man_procent = summary[1].find('b').text
    print ("Процент мужиков ", man_procent)
    print ("++++++++++++++++++++++++++++++++++++++")
    print ("Кандидаты:")

    chapter_section_3 = chapter__sections[2]
    deputats_body = chapter_section_3.find('tbody')
    deputat_items = deputats_body.find_all('tr')

    for item in deputat_items:
        person = item.find('div', class_="person-item person-item_row js-popup-trigger")
        person_span = person.find_all('span')

        _name = person_span[0].text
        _fraction = Fraction.objects.get(name=person_span[1].text)
        _post = item.findall('p', class_="js-foldable")[0]['data-fulltext']
        print ("Имя ", _name)
        print ("Фракция ", _fraction.name)
        print ("Должность ", _post)

def main():
    html = get_html("https://election.novayagazeta.ru/region/54701000000/")
    get_page_data(html)


if __name__ == '__main__':
    main()
