import requests
from bs4 import BeautifulSoup


url = 'http://duma.gov.ru/duma/persons/99112808/'
r = requests.get(url)
with open('test.html', 'w') as output_file:
  output_file.write(r)
