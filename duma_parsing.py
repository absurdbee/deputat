import requests


url = 'http://duma.gov.ru/duma/persons/99112808/'
r = requests.get(url)
print r
