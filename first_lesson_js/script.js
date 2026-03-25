const SHIP_NAME = 'X01 - "First"';
let fuelLevel = 100;
let isEngineStarted = false;
let missionStatus;
let lastError = null;

let captain = prompt('Введите имя капитана');
console.log(`${captain.toUpperCase()}, привтствую вас, вы капитана корабля ${SHIP_NAME}`);

let crew = Array(captain, 'Иван', 'Василий');
crew.unshift('Сергей');
crew.pop();
console.log(`В экипаже сейчас ${crew.length}`);

function checkFuel(amount) {
    if (amount >= fuelLevel) {
        return true;
    } else {
        return false;
    }
}

let tasks = Array('проверить шлюз', 'починить робота', 'сварить кофе');

for (let i = 0; i < tasks.length; i++) {
    if (tasks[i].includes('кофе')) {
        console.log(`${i+1}. ${tasks[i]} - Приоритетно!`);
    } else {
        console.log(`${i+1}. ${tasks[i]}`);
    }
}