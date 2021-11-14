const fs = require('fs');

const update = (lastData) => {
    let data = JSON.stringify(lastData, null, 4);
    fs.writeFileSync('./data.json', data);
}

module.exports = update;