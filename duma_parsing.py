import requests
from bs4 import BeautifulSoup


url = 'https://habr.com/ru/post/280238/'
r = requests.get(url)
with open('test.html', 'w') as output_file:
  output_file.write(r.text)
