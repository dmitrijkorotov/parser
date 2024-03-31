import requests
import bs4
import json
from fake_headers import Headers


def get_headers():
    return Headers(os='win', browser='chrome').generate()

def info_vacancy(link):
    result = []
    responce = requests.get(link, headers=get_headers())
    main_html_data = responce.text
    soup = bs4.BeautifulSoup(main_html_data, features='lxml')
    vacancies = soup.find_all('div', class_='vacancy-serp-item-body')
    for vacancy in vacancies:
        link = vacancy.find('a', class_='bloko-link').get('href')
        company = vacancy.find('div', 
                            class_="vacancy-serp-item__meta-info-company").text
        company = company.replace('\xa0',' ')
        city = vacancy.find('div', class_='vacancy-serp-item__info').text
        
        if city.find('Москва') > -1:
            city = 'Москва'
        elif city.find('Санкт-Петербург') > -1:
            city = 'Санкт-Петербург'
        
        try:
            salary = vacancy.find('span', class_="bloko-header-section-2").text
        except:
            salary = 'зп не указана'
        
        result.append({'link': link ,
                       'salary': salary, 
                       'company': company,
                       'city': city})
    return result

def save_data(data):
    with open('result_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    data = info_vacancy('https://spb.hh.ru/search/vacancy?text=python+django+\
                        flask&salary=&ored_clusters=true&area=1&area=2&hhtmFro\
                        m=vacancy_search_list&hhtmFromLabel=vacancy_search_line')
    save_data(data)