import random
import math
AMOUNT = 10

# ОСОБЕННОСТЬ JS - функция генератор
def getRandomItem(arr):

    prevIndices = set()

    while (prevIndices.__len__() != AMOUNT):
        index = getRandomNumberInRange(0, AMOUNT - 1)

        # ОСОБЕННОСТЬ JS: строковая интерполяция
        print(
            f'index=${index}'
        )

        if (prevIndices.__contains__(index)):
            continue
        
        prevIndices.add(index)

        # ОСОБЕННОСТЬ JS: строковая интерполяция
        print(
            f'arr[index]=${arr[index]}'
        )

        # ОСОБЕННОСТЬ JS: ключевое слово yield -
        # в отличие от return - yield позволяет продолжить
        # выполнение генератора
        yield arr[index]
    


# случайное число в диапазоне [min max]
def getRandomNumberInRange(min, max):

        return math.floor(random.random() * (max - min + 1)) + min


numbers = []

for i in range(0, AMOUNT, 1): 
    numbers.append(i)


numbersRandomized = []
iterator = getRandomItem(numbers)

# ОСОБЕННОСТЬ JS: перебор генератора 
for value in iterator:
    numbersRandomized.append(value)


for i in range(0, AMOUNT, 1): 
    print(
        f'numbers[${i}] = ${numbers[i]}\nnumbersRandomized[${i}] = ${numbersRandomized[i]}'
    )

