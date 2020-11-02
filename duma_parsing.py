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

id_list = ['99112869', '1055917', '99100145', '99100829', '99104023', '99100750', '99111093', '99112790', '99111912',
           '99112757', '99112791', '99111789', '99112121', '99112864', '99112752', '99112778', '99111850', '99112871',
           '99112936', '99112608', '99109636', '99112642', '99112915', '99110033', '99112430', '99112795', '99111793',
           '99112894', '99110020', '99100110', '99113129', '99112873', '99112824', '99112926', '99112734', '99112813',
           '99112847', '99112899', '99112739', '99112921', '99112912', '99111922', '99112721', '99112760', '99111883',
           '99112938', '99112037', '99111798', '99112885', '99112930', '99112844', '99110933', '99111820', '99112730',
           '99110089', '99112723', '99112799', '99112729', '99111084', '99112914', '99112925', '99112851', '99107708',
           '99112753', '99112843', '99100171', '99110050', '99110911', '99111018', '99111543', '99112828', '99111779',
           '99100788', '99112834', '99112835', '99110941', '99112815', '99112770', '99112728', '99112916', '99112929',
           '99112798', '99112755', '99112028', '99100654', '99112883', '99112863', '99112762', '99111945', '99105318',
           '99100601', '99112829', '99100319', '99111967', '99109949', '99111791', '99100158', '99112841', '99111054',
           '99112886', '99112005', '99112023', '99109613', '1055897', '99112772', '99100295', '99112861', '99112817',
           '99112485', '99100315', '99111877', '99103226', '99107007', '99100666', '99105719', '99102119', '99111067',
           '99111399', '99109906', '99112850', '99111374', '99112737', '99112796', '99111086', '99111930', '99112882',
           '99109942', '99110949', '99111035', '99112126', '99111010', '99110102', '99112175', '99112011', '99109895',
           '99107687', '99100799', '99112003', '99100784', '99109943', '99112573', '99100761', '99112896', '99111854',
           '99112009', '99109998', '99111801', '99112800', '1055902', '99112845', '99111931', '99112012', '99112920',
           '99112010', '99112853', '99112775', '99112127', '99111981', '99110934', '99111795', '99111951', '99100790',
           '99112712', '99109953', '99109957', '99112768', '99110096', '99111809', '99110097', '1055893', '99111992',
           '99112719', '1055891', '99112735', '99109921', '99111832', '99112875', '99111867', '99111220', '99112839',
           '99112832', '99112763', '99112466', '99110990', '99112650', '99103008', '99111855', '99112812', '99112751',
           '99109900', '99112893', '99112039', '99110929', '99112732', '1055890', '99112764', '99112776', '99111827',
           '99110957', '99112738', '99101528', '99112362', '99110958', '99112823', '99112867', '99112015', '1055896',
           '99112794', '99112001', '99112822', '99112740', '99112726', '99112858', '99112120', '99112685', '99111859',
           '99111977', '99112784', '99112889', '99112819', '99111888', '99111733', '99111057', '99111920', '99110085',
           '99100316', '99112769', '1055889', '99112895', '99100416', '99112750', '99112857', '99112797', '99112773',
           '99111064', '99112789', '99112759', '99110914', '99112745', '99112779', '99111704', '99109956', '99100407',
           '99110932', '99112014', '99104631', '99112511', '99100248', '99111892', '99112781', '99112814', '99112481',
           '99111873', '99112831', '99111950', '99111836', '99112887', '99112806', '99111061', '99112711', '99112837',
           '99112830', '99112842', '99112725', '99112761', '99112025', '99111787', '99112736', '99110948', '99112000',
           '99113072', '99100142', '99111048', '99112722', '99110921', '99112748', '99112805', '99112724', '1055899',
           '99112917', '99112788', '99112787', '99112892', '99112854', '99111929', '99112007', '99110982', '99112810',
           '99112754', '99112710', '99112816', '99109798', '99111852', '99112870', '99111049', '99111015', '99112742',
           '99112820', '99112826', '99111991', '99112242', '99112808', '99112741', '99111812', '99110299', '99112577',
           '99112802', '99109598', '99112513', '99112105', '99110082', '99112021', '99112860', '99112746', '99112777',
           '99112878', '99112891', '99111936', '99109600', '99100776', '1055895', '99111833', '99110999', '99112236',
           '99112649', '99112933', '99112432', '99100700', '99112774', '99107896', '99112935', '99109653', '99112783',
           '99111063', '99100749', '99100640', '99112483', '99112766', '99109963', '99100888', '99100696',
           '99112749', '99111028', '99110967', '99111778', '99109981', '99112771', '99112848', '99112879', '99112792',
           '99112928', '99110985', '99112927', '99111079', '99112934', '99111948', '99110213', '99100522', '99111939',
           '99100972', '99111893', '99112803', '99112922', '99110954', '99102051', '99112840', '99112758', '99112862',
           '99107264', '99112727', '99112918', '99112743', '99112855', '99112849', '99112911', '99112782', '99111645',
           '99112859', '99112913', '99112811', '99112807', '99100886', '99112877', '99112825', '99112868', '1055473',
           '99100781', '99112018', '99112866', '99112880', '99112874', '99112890', '99110909', '1055901', '99100862',
           '99112924', '99111804', '99112809', '99112780', '99112937', '99111844', '99112876', '99111831',
           '99110927', '99100398', '99100052', '1055905', '99112032', '99112897', '99112919', '99112821', '99111961',]


def get_html(url):
    r = requests.get(url)
    return r.text

def get_file(url):
    r = requests.get('http://duma.gov.ru' + url, stream=True)
    return r

def get_name(url):
    name = url.split('/')[-1]
    return name

def save_image(name, file_object):
    with open(name, 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)


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
    elect_image = save_image(get_name(image['src']), get_file(image['src']))

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
    for id in id_list:
        url = 'http://duma.gov.ru/duma/persons/' + id + "/"
        html = get_html(url)
        data = get_page_data(html)
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
