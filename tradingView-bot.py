import os
import time
from datetime import datetime
import json
from webhook import Webhook
from colorama import Fore, Back, Style
import colorama

colorama.init()


class TradingView():
    def __init__(self, coin_name) -> None:
        self.coin_currency = coin_name

    def startLoop(self):
        while True:
            self.checkResponse()
            time.sleep(10)
    # def startLoop(self):
    #     # color: rgb(76, 175, 80); => Green
    #     # color: rgb(255, 82, 82); => Red
    #     while True:
    #         try:
    #             time.sleep(8)
    #             page_source = self.driver.page_source
    #             # "//div[style='color: rgb(255, 82, 82);']"
    #             if 'rgb(76, 175, 80)' in page_source or 'rgb(255, 82, 82)' in page_source:
    #                 if 'rgb(76, 175, 80)' in page_source:
    #                     value = self.driver.find_element_by_xpath(
    #                         "//div[@style='color: rgb(76, 175, 80);']")
    #                 elif 'rgb(255, 82, 82)' in page_source:
    #                     value = self.driver.find_element_by_xpath(
    #                         "//div[@style='color: rgb(255, 82, 82);']")
    #                 # **** #
    #                 if value is not None:
    #                     # self.coin_currency = self.driver.find_element_by_class_name(
    #                     #     'tv-chart-view__symbol-link').text
    #                     self.coin_currency = self.coin_name
    #                     # value = self.driver.find_element_by_xpath("//div[@style='color: rgb(76, 175, 80);']")
    #                     # if value is None:
    #                     #     value = self.driver.find_element_by_xpath("//div[@style='color: rgb(255, 82, 82);']")
    #                     color = value.get_attribute('style')
    #                     now = datetime.now()
    #                     data = {
    #                         "value": value.text,
    #                         "coin_currency": self.coin_currency,
    #                         "chart_url": self.url,
    #                         "day": now.day,
    #                         "hour": now.hour,
    #                         "minute": now.minute
    #                     }
    #                     if color == 'color: rgb(76, 175, 80);':
    #                         print(Fore.GREEN,
    #                               f'{self.coin_currency}:', value.text)
    #                         print(Style.RESET_ALL)
    #                         data['color'] = 'green'
    #                         self.checkResponse(data)
    #                     elif color == 'color: rgb(255, 82, 82);':
    #                         data['color'] = 'red'
    #                         print(
    #                             Fore.RED, f'{self.coin_currency}:', value.text)
    #                         print(Style.RESET_ALL)
    #                         self.checkResponse(data)
    #                     else:
    #                         print('İnner Error!')
    #                         self.driver.get(self.url)
    #                     # time.sleep(10)
    #             else:
    #                 print('Outer Error!')
    #                 self.driver.get(self.url)

    #         except Exception as err:
    #             print(err)
    #             self.repairLastData()
    #             self.driver.get(self.url)

    def repairLastData(self):
        with open('lastData.json', 'w', encoding='UTF-8') as file:
            file.write('{}')
        # with open('lastData.json', encoding='UTF-8') as file:
        #     lastData = file.read()
        # lastData = {}
        #     json.dump(lastData, file, indent=4)

    def checkTime(self, lastData):
        now = datetime.now()
        last = datetime(now.year, now.month, lastData[2],
                        lastData[0], lastData[1])
        duration = now - last
        duration_in_s = duration.total_seconds()
        minutes = divmod(duration_in_s, 60)[0]

        # print('Minutes:', minutes)
        if minutes > 240:
            return True
        else:
            return False

    def checkResponse(self):
        with open('./coin-data/data.json', encoding='UTF-8') as file:
            data = json.load(file)
        with open('lastData.json', encoding='UTF-8') as file:
            lastData = json.load(file)

        coinData = data[self.coin_currency]

        now = datetime.now()
        _data = {
            "value": coinData['value'],
            "coin_currency": self.coin_currency,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute
        }
        if coinData['color'] == 1:
            _data['color'] = 'green'
            print(Fore.GREEN,
                  f'{self.coin_currency}:', _data['value'])
            print(Style.RESET_ALL)
        elif coinData['color'] == 2:
            _data['color'] = 'red'
            print(Fore.RED,
                  f'{self.coin_currency}:', _data['value'])
            print(Style.RESET_ALL)

        if self.coin_currency in lastData:

            time_data = [
                lastData[self.coin_currency]['hour'],
                lastData[self.coin_currency]['minute'],
                lastData[self.coin_currency]['day']
            ]
            if _data['color'] != lastData[self.coin_currency]['color']:
                first_run = None
                if 'first_run' in lastData[self.coin_currency]:
                    first_run = lastData[self.coin_currency]['first_run']
                lastData[self.coin_currency] = _data
                with open('lastData.json', 'w', encoding='UTF-8') as file:
                    json.dump(lastData, file, indent=4)

                if first_run is not None:
                    if first_run is True:
                        Webhook(_data).sendMessage()

                elif self.checkTime(time_data) == True:
                    print('sa')
                    Webhook(_data).sendMessage()
                elif self.checkTime(time_data) == False:
                    lastData[self.coin_currency]['hour'] = time_data[0]
                    lastData[self.coin_currency]['minute'] = time_data[1]
                    lastData[self.coin_currency]['day'] = time_data[2]

                    if lastData[self.coin_currency]['color'] == 'green':
                        lastData[self.coin_currency]['color'] = 'red'

                    elif lastData[self.coin_currency]['color'] == 'red':
                        lastData[self.coin_currency]['color'] = 'green'
                    print('as')
                with open('lastData.json', 'w', encoding='UTF-8') as file:
                    json.dump(lastData, file, indent=4)
        else:
            _data['first_run'] = True
            lastData[self.coin_currency] = _data
            with open('lastData.json', 'w', encoding='UTF-8') as file:
                json.dump(lastData, file, indent=4)

            # Webhook(_data).sendMessage()

        with open('lastData.json', 'w', encoding='UTF-8') as file:
            json.dump(lastData, file, indent=4)


with open('./coin-data/charts.json', encoding='UTF-8') as file:
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

TradingView(coin_name).startLoop()
