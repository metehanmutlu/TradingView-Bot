from selenium import webdriver
import os
import time
import json
from webhook import Webhook


class TradingView():
    def __init__(self, url, coin_name) -> None:
        self.url = url
        self.coin_name = coin_name
        path = os.path.abspath('chromedriver.exe')
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.get(self.url)
        time.sleep(2)

    def startLoop(self):
        # color: rgb(76, 175, 80); => Green
        # color: rgb(255, 82, 82); => Red
        while True:
            try:
                time.sleep(8)
                values = self.driver.find_elements_by_class_name(
                    'valueValue-2KhwsEwE')
                if values is not None:
                    # self.coin_currency = self.driver.find_element_by_class_name(
                    #     'tv-chart-view__symbol-link').text
                    self.coin_currency = self.coin_name
                    value = values[-2].text
                    color = values[-2].get_attribute('style')
                    data = {
                        "value": value,
                        "coin_currency": self.coin_currency,
                        "chart_url": self.url
                    }
                    if color == 'color: rgb(76, 175, 80);':
                        print('Green', value)
                        data['color'] = 'green'
                        self.checkResponse(data)
                    elif color == 'color: rgb(255, 82, 82);':
                        data['color'] = 'red'
                        print('Red', value)
                        self.checkResponse(data)
                    else:
                        print('İnner Error!')
                        self.driver.get(self.url)

                    # time.sleep(10)
                else:
                    print('Outer Error!')
                    self.driver.get(self.url)

            except KeyboardInterrupt:
                self.driver.close()

    def checkResponse(self, data):
        with open('lastData.json', encoding='UTF-8') as file:
            lastData = json.load(file)

        if self.coin_currency in lastData:
            if data['color'] != lastData[self.coin_currency]['color']:
                lastData[self.coin_currency] = data

                Webhook(data).sendMessage()
        else:
            lastData[self.coin_currency] = data

            # Webhook(data).sendMessage()
        with open('lastData.json', 'w', encoding='UTF-8') as file:
            json.dump(lastData, file, indent=4)


with open('charts.json', encoding='UTF-8') as file:
    charts = json.load(file)

coin_text = ''

for i, coin in enumerate(charts, start=1):
    coin_text += f'{i}) {coin}\n'
else:
    message_text = f'\n\n**Seçmek istediğiniz coinin numarasını giriniz**\n\n{coin_text}'
    print(message_text)

coin_id = int(input('Coin No: '))
for i, coin in enumerate(charts, start=1):
    if i == coin_id:
        coin_name = coin
        break

TradingView(charts[coin_name]['url'], coin_name).startLoop()
