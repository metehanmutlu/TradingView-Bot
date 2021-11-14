const date = new Date();
const moment = require('moment');


const checkTime = (lastData) => {
    const last = moment(
        `${date.getFullYear()}-${date.getMonth() + 1}-${lastData[0]} ${lastData[1]}:${lastData[2]}`,
        'YYYY-M-DD HH:mm'
    );
    const now = moment(
        `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`,
        'YYYY-M-DD HH:mm'
    );

    const minutesDiff = now.diff(last, 'minutes');
    console.log(date.getMinutes());
    if (minutesDiff > 1) {
        return true;
    } else {
        return false;
    }
}

module.exports = checkTime;