const marketAPI = require('@mathieuc/tradingview');
const readLastData = require('./modules/readLastData');
const updateData = require('./modules/updateLastData');
// const inputInterface = require('./modules/createInputInterface');
const readCoins = require('./modules/readCoins');


const coins = readCoins();

const market = marketAPI(false);

for (const [key, value] of Object.entries(coins)) {
    market.on('logged', () => {
        market.initChart({
            symbol: key,
            period: '240',
            range: 1,
            indicators: [
                { name: 'Tilson T3', id: 'PUB;pzHF3syecckZAXs6XEdJ3ovqWvaEw9CV', version: '2' }
            ]
        }, (periods) => {
            const indicator = periods[0]['Tilson T3'];
            const _value = Object(indicator).Plot;
            const _color = Object(indicator)._plot_1;
            if (_value != undefined && _color != undefined) {
                const data = {
                    value: _value,
                    color: _color,
                    coinCurrency: key
                }
                let lastData = readLastData();
                lastData[key] = data;
                updateData(lastData);
                // console.log(_value, _color);
            }
        })
        console.log(`${key} Started....`);
    })
}