import sys,os
import re
import requests
from bs4 import BeautifulSoup

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from lists.models import *
from elect.models import *

def get_html(url):
    r = requests.get(url)
    return r.text

def get_links(url):
    soup = BeautifulSoup(url, 'lxml')
    list = []
    container = soup.find('section', class_='list-persons__wrapper js-deputies-wrapper')
    blocks = container.find_all('a', class_='person__image-wrapper person__image-wrapper--s')
    for item in blocks:
        list += ['http://duma.gov.ru' + item['href'], ]
    return list


def get_educations_for_elect(html, elect):
    soup = BeautifulSoup(html, 'lxml')
    try:
        definitions_list_2 = soup.find('dl', class_='definitions-list definitions-list--capitalize')
        edu_count = 0
        edu_dd = definitions_list_2.find_all('dd')
        edu_dt = definitions_list_2.find_all('dt')
        for dd in edu_dd:
            EducationElect.objects.create(elect=elect, title=edu_dd[edu_count].text, year=edu_dt[edu_count].text)
            edu_count += 1
    except:
        pass

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    # name
    name = soup.find('h1', class_='article__title--person')
    if name:
        _name = str(name)
        _name = _name.replace('\n', '').replace('<h1 class="article__title article__title--person">', '').replace('<br/>', ' ').replace('</h1>', '')
    else:
        name = soup.find('h2', class_='person__title person__title--l')
        _name = str(name)
        _name = _name.replace('\n', '').replace('<h2 class="person__title person__title--l"><span itemprop="name">', '').replace('<br/>', ' ').replace('</span></h2>', '').replace('</h2>', '')

    #description
    description = soup.find('div', class_='article__lead article__lead--person')
    if not description:
        description = soup.find('div', class_='page__lead')
    description = description.text

    #image
    image = soup.find('img', class_='person__image person__image--mobile')
    if not image:
        image = soup.find('img', class_='person__image person__image--l')

    #birthday, authorization
    content__s = soup.find('div', class_='content--s')
    birthday = content__s.find_all('p')[0].text
    birthday = birthday.replace('Дата рождения: ', '')
    authorization = content__s.find_all('p')[1].text
    authorization = authorization.replace('\n', '').strip().replace('Дата вступления в полномочия:                                 ', '')

    #election_information
    definitions_list_1 = soup.find_all('dl', class_='definitions-list')[0]
    dd_1 = definitions_list_1.find('dd')
    election_information = dd_1.find_all('p')[0].text + definitions_list_1.find('dt').text
    election_information = election_information.replace('\n', '').strip().replace('                   ', ':')

    #fraction
    person__description = soup.find('div', class_='person__description__grid')
    fraction = person__description.find('a', class_='person__description__link').text

    try:
        region_list = soup.find_all('div', class_='person__description__col')[3].text.replace(", ", ",")
    except:
        region_list = []

    data = {'name': _name,
            'fraction': fraction.replace("\xa0", " "),
            'elect_image': 'http://duma.gov.ru' + image['src'],
            'description': description,
            'region_list': region_list,
            'birthday': birthday,
            'election_information': election_information,
            'authorization': authorization}
    return data


def main():
    html = get_html("http://duma.gov.ru/duma/deputies/")
    lists = get_links(html)
    for url in lists:
        html = get_html(url)
        data = get_page_data(html)
        try:
            regions_query = data["region_list"].split(",")
            for region_name in regions_query:
                if Region.objects.filter(name=region_name).exists():
                    pass
                else:
                    region = Region.objects.create(name=region_name)
        if not Elect.objects.filter(name=data["name"]).exists():
            if data["fraction"] == '«ЕДИНАЯ РОССИЯ»':
                current_fraction = Fraction.objects.get(slug="edinaya_russia")
            elif data["fraction"] == "СПРАВЕДЛИВАЯ РОССИЯ":
                current_fraction = Fraction.objects.get(slug="spravedlivaya_russia")
            elif data["fraction"] == "КПРФ":
                current_fraction = Fraction.objects.get(slug="kprf")
            elif data["fraction"] == "ЛДПР":
                current_fraction = Fraction.objects.get(slug="ldpr")
            elif data["fraction"] == "Депутаты, не входящие во фракции":
                current_fraction = Fraction.objects.get(slug="no_fraction")

            new_elect = Elect.objects.create(name=data["name"], description=data["description"], birthday=data["birthday"], authorization=data["authorization"], election_information=data["election_information"], fraction=current_fraction)
            regions_query = data["region_list"]
            if regions_query:
                regions_query = data["region_list"].split(",")
                for region_name in regions_query:
                    try:
                        region = Region.objects.get(name=region_name)
                        region.elect_region.add(new_elect)
                    except:
                        pass
            new_elect.get_remote_image(data["elect_image"])
            list = AuthorityList.objects.get(slug="state_duma")
            list.elect_list.add(new_elect)
            get_educations_for_elect(html, new_elect)
            print(data["name"])

if __name__ == '__main__':
    main()
