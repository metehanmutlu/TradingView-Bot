const prompt = require('prompt-sync')();
const fs = require('fs');

const readCoins = () => {
    let rawdata = fs.readFileSync('./charts.json');
    let coins = JSON.parse(rawdata);
    return coins
}

const coins = readCoins()
let coinText = ''
let i = 0
let k = 0

for (const [key, value] of Object.entries(coins)) {
    i++;
    coinText += `${i}) ${key}\n`;
}
const messageText = `\n\n**Seçmek istediğiniz coinin numarasını giriniz**\n\n${coinText}`
console.log(messageText);

const coinId = prompt('Coin No: ');
for (const [key, value] of Object.entries(coins)) {
    k++;
    if (k == Number(coinId)) {
        var coinName = key;
        break;
    }
}

module.exports = coinName;