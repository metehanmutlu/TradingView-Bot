const fs = require('fs');

const readCoins = () => {
    let rawdata = fs.readFileSync('./charts.json');
    let coins = JSON.parse(rawdata);
    return coins
}

module.exports = readCoins;