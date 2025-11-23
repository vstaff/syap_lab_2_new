import json
# ОСОБЕННОСТЬ JS: декораторы - инструменты для расширения возможностей 
# функций в JavaScript
def myCacheDecorator(func):

    # ОСОБЕННОСТЬ JS: Map - ассоциативный массив
    # здесь этот ассоциативный массив будет выполнять роль кэша
    # он позволит ускорить работу функции, так как не придется пересчитывать
    # уже посчитанные значения функций 
    cache = dict()

    def innerFunc(*args):

        # ОСОБЕННОСТЬ JS: json.dumps - преобразует javascript-объект в строку
        # необходимо это для того, чтобы декоратор работал единым образом,
        # независимо от характера и количества аргументов декорируемой функции
        key = json.dumps(args)

        # если в кеше уже подсчитана функция для этих аргументов
        # - просто возвращаем результат из хранилища
        if (cache.__contains__(key)):
            return cache.get(key)
        
        result = func(*args)
        cache.setdefault(key, result)
        return result
    

    return innerFunc


# функция для подсчета n-ого числа Фибоначчи
def myFibonacci(n):

    # проверка на то, чтобы n был положительным целым числом
    if (n <= 0):
        raise Exception("expected positive integer")
    

    # базовый случай рекурсии
    if (n <= 2):
        return 1
    

    return myFibonacci(n - 1) + myFibonacci(n - 2)


# применяем декоратор для ускорения работы функции
myFibonacci = myCacheDecorator(myFibonacci)

# без декоратора - подсчет 100 чисел Фибоначчи 
# затянулся бы на очень долго время где-то на 60-70 элементе 
# (если не раньше)
for i in range(1, 100, 1): 
    print(myFibonacci(i))

