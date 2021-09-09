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

from district.models import District2
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

    _list = AuthorityList.objects.get(name="Кандидат в депутаты гос. думы")

    tgrids = soup.find_all('div', class_='tgrid')
    parth = 0
    for tgrid in tgrids:
        if not Okrug.objects.filter(name=h5_list[h5_count].text, region=region).exists():
            okrug = Okrug.objects.create(name=h5_list[h5_count].text, region=region)
        else:
            okrug = Okrug.objects.get(name=h5_list[h5_count].text, region=region)

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
                else:
                    _patr = Fraction.objects.get(slug="no_fraction")

                deps = item.find_all('li')
                if not Elect.objects.filter(name=name, region=region, okrug=okrug).exists():
                    elect = Elect.objects.create(
                                    name=name.text,
                                    okrug=okrug,
                                    post_2=item.find("p", class_='fio').text.replace(name + ", ",""),
                                    birthday=deps[1].text.replace("Возраст: ","");
                                    description=deps[2].text.replace("Образование: ",""),
                                    fraction=_patr
                                )
                    if item.find("img")["src"] == "/wp-content/uploads/imagefb.jpg":
                        img = 'https://служународу.рус/static/images/elect_image.png'
                    else:
                        img = "https://gosduma-2021.com/" + item.find("img")["src"]
                    elect.get_remote_image(img)
                    elect.region.add(region)
                    elect.list.add(_list)
                    print(elect.name, " добавлен!")
                else:
                    elect = Elect.objects.get(name=name, region=region, okrug=okrug)
                    print(elect.name, " уже есть!")
            count += 1
            print("--------------------")
        print("=======================")

def main():
    html = get_html("https://gosduma-2021.com/s/volgogradskaya-oblast/")
    get_page_data(html, region)

if __name__ == '__main__':
    main()
