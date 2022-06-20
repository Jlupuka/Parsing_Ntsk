import requests
from bs4 import BeautifulSoup
import json

class Parsing:
    def __init__(self, src):
        self.src = src
        self.soup = BeautifulSoup(self.src, 'lxml')
        self.dict_ = dict()

    def parsing_exchange(self):
        articles = self.soup.find('div', class_="exchange")
        find_USD = articles.find('div', class_="exchange-item down").text.replace(' USD ', '').replace(' ', '')
        find_EURO = articles.find('div', class_="exchange-item up").text.replace(' EURO ', '').replace(' ', '')
        self.dict_['USD'], self.dict_['EURO'] = find_USD, find_EURO


    def parsing_weather(self):
        articles = self.soup.find('div', class_="weather")
        temp = articles.find_all('span', class_="temp")
        now = temp[0].text.replace(' ', '')
        night = temp[1].text.replace(' ', '')
        weather_info_acrtive = self.soup.find('div', class_="s11 weather-info active").text
        weather_info_acrtive = weather_info_acrtive.replace(': ', '\n').replace('\t', '').split('\n')
        weather_info_acrtive = list(filter(None, weather_info_acrtive))

        self.dict_['Температура сейчас'], self.dict_['Температура ночью'] = now, night
        self.dict_['Давление'] =  ''.join(weather_info_acrtive[1]).strip()
        self.dict_['Ветер'] =  ''.join(weather_info_acrtive[3]).strip()
        self.dict_['Влажность'] = ''.join(weather_info_acrtive[-1]).strip()

    def save_in_json(self):
        with open('Parse_exchange_and_weather_Ntsk.json', 'w', encoding='utf-8') as f:
            json.dump(self.dict_, f, indent=4, ensure_ascii=False)
        print('Saved!')


def data(url):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = requests.get(url, headers=headers)
    src = req.text
    # with open('index.html', 'w', encoding='utf-8') as f:
    #     f.write(src)
    return src


url = 'https://ntsk.ru/'
pars = Parsing(data(url))
pars.parsing_exchange()
pars.parsing_weather()
pars.save_in_json()