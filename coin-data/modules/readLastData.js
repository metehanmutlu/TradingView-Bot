const fs = require('fs');

const readLastData = () => {
    let rawdata = fs.readFileSync('./data.json');
    let lastData = JSON.parse(rawdata);
    return lastData
}

module.exports = readLastData;