import requests


url = 'http://duma.gov.ru/duma/persons/99112808/'
r = requests.get(url)
with open('test.html', 'w') as output_file:
  output_file.write(r.text.encode('cp1251'))
