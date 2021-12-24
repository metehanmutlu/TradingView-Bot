import json

coin_name = input('Coin Type (BTCUSDT): ')

with open('./coin-data/charts.json', encoding='UTF-8') as file:
    charts = json.load(file)

if coin_name not in charts:
    charts[coin_name] = {}

# charts[coin_name]['url'] = coin_link

with open('./coin-data/charts.json', 'w', encoding='UTF-8') as file:
    json.dump(charts, file, indent=4)

input('Coin Added !\nEnter...')
