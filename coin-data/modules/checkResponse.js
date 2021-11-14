const readLastData = require('./readLastData');
const updateData = require('./updateLastData');
const checkTime = require('./checkTime')

const checkResponse = (data) => {
    let lastData = readLastData();
    if (lastData.hasOwnProperty(data.coinCurrency)) {
        const time_data = [
            lastData[data.coinCurrency].day,
            lastData[data.coinCurrency].hour,
            lastData[data.coinCurrency].minute
        ]
        if (data.color != lastData[data.coinCurrency].color) {
            let first_run = null;
            if (lastData[data.coinCurrency].hasOwnProperty('first_run')) {
                first_run = lastData[data.coinCurrency]['first_run']
            }
            lastData[data.coinCurrency] = data;
            console.log('1');
            updateData(lastData);

            if (first_run !== null) {
                if (first_run == true) {
                    console.log('Alert Sended!');
                }
            } else if (checkTime(time_data) == true) {
                console.log('Alert Sended true!');

            } else if (checkTime(time_data) == false) {
                console.log('false');
                lastData[data.coinCurrency].hour = time_data[1]
                lastData[data.coinCurrency].minute = time_data[2]

                if (lastData[data.coinCurrency].color == 'green') {
                    lastData[data.coinCurrency].color = 'red';
                } else if (lastData[data.coinCurrency].color == 'red') {
                    lastData[data.coinCurrency].color = 'green'
                }
            }
            console.log('2');
            updateData(lastData);
        }
    } else {
        data['first_run'] = true;
        lastData[data.coinCurrency] = data
        console.log('3');
        updateData(lastData);
    }
    
}

module.exports = checkResponse;