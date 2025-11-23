// ОСОБЕННОСТЬ JS: декораторы - инструменты для расширения возможностей 
// функций в JavaScript
function myCacheDecorator(func) {
  // ОСОБЕННОСТЬ JS: Map - ассоциативный массив
  // здесь этот ассоциативный массив будет выполнять роль кэша
  // он позволит ускорить работу функции, так как не придется пересчитывать
  // уже посчитанные значения функций 
  const cache = new Map();

  return (...args) => {
    // ОСОБЕННОСТЬ JS: JSON.stringify - преобразует javascript-объект в строку
    // необходимо это для того, чтобы декоратор работал единым образом, 
    // независимо от характера и количества аргументов декорируемой функции
    const key = JSON.stringify(args);
    
    // если в кеше уже подсчитана функция для этих аргументов 
    // - просто возвращаем результат из хранилища 
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = func(...args);
    cache.set(key, result);
    return result;
  }
}

// функция для подсчета n-ого числа Фибоначчи
function myFibonacci(n) {
  // проверка на то, чтобы n был положительным целым числом
  if (!(Number.isInteger(n)) || n <= 0) {
    throw new Error("expected positive integer");
  }

  // базовый случай рекурсии
  if (n <= 2) {
    return 1;
  }

  return myFibonacci(n - 1) + myFibonacci(n - 2);
}

// применяем декоратор для ускорения работы функции
myFibonacci = myCacheDecorator(myFibonacci)

// без декоратора - подсчет 100 чисел Фибоначчи 
// затянулся бы на очень долго время где-то на 60-70 элементе 
// (если не раньше)
for (let i = 1; i < 100; i++) {
  console.log(myFibonacci(i));
}
