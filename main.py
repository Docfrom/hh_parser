import bs4
import requests
from fake_headers import Headers
import json

def get_headers():
    return Headers(os='win', browser='chrome').generate()


response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers())
html_data = response.text
soup = bs4.BeautifulSoup(html_data, features='lxml')
divs = soup.find_all('div', class_='serp-item')


result = []
for div in divs:
  tag_a = div.a
  job_link = tag_a['href']


  span_title = tag_a.contents[0]


  job_title: str = span_title.contents[0]
  if not("django" in job_title.lower() or "flask" in job_title.lower()):
    continue


  vilka = "не указана"
  spans = div.find_all(attrs={"data-qa": 'vacancy-serp__vacancy-compensation'})
  for span in spans:
        vilka = " ".join(span.contents)

  employer = "Не укзаано"
  for a in div.find_all(attrs={"data-qa":"vacancy-serp__vacancy-employer"}):
      employer = " ".join(a.find("span").contents)

  city = 'Не указан'
  for child_div in  div.find_all(attrs={"data-qa": "vacancy-serp__vacancy-address"}):
      if child_div.name == "div":
        city = child_div.contents[0]
      else:
        city = child_div.contents[0].contents[0]


  result.append({"title": job_title,
                "salary": vilka,
                "link": job_link,
                "employer": employer,
                "city": city})


string_to_write = json.dumps(result)
with open("result.txt", mode="w") as file:
  file.write(string_to_write)


# with open("result.txt") as file:
#   string = file.readline()
#   offers = json.loads(string)
#   for offer in offers:
#     print(f'Должность: {offer["title"]}\nВилка: {offer["salary"]}\nURL: {offer["link"]}\nНаниматель: {offer["employer"]}\nГород:  {offer["city"]}')
#     print("--"*10)