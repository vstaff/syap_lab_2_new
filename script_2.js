const AMOUNT = 10;

// ОСОБЕННОСТЬ JS - функция генератор
function* getRandomItem(arr) {
  const prevIndices = new Set();

  while (prevIndices.size != AMOUNT) {
    const index = getRandomNumber(0, AMOUNT - 1);

    // ОСОБЕННОСТЬ JS: строковая интерполяция
    console.log(
      `index=${index}`
    )

    if (prevIndices.has(index)) {
      continue;
    };
    prevIndices.add(index);

    // ОСОБЕННОСТЬ JS: строковая интерполяция
    console.log(
      `arr[index]=${arr[index]}`
    )

    // ОСОБЕННОСТЬ JS: ключевое слово yield -
    // в отличие от return - yield позволяет продолжить
    // выполнение генератора
    yield arr[index];
  }
}

// случайное число в диапазоне [min; max]
// ОСОБЕННОСТЬ JS: стрелочная функция (на Python можно воспользоваться lambda выражениями)
const getRandomNumber = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const numbers = [];

for (let i = 0; i < AMOUNT; i++) {
  numbers.push(i);
}

const numbersRandomized = [];
const iterator = getRandomItem(numbers);

// ОСОБЕННОСТЬ JS: перебор генератора 
for (const value of iterator) {
  numbersRandomized.push(value);
}

for (let i = 0; i < AMOUNT; i++) {
  console.log(
    `numbers[${i}] = ${numbers[i]}\nnumbersRandomized[${i}] = ${numbersRandomized[i]}`
  );
}
