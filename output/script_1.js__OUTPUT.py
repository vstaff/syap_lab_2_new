class MyNode:
    # ОСОБЕННОСТЬ JS: реализаций приватных свойств и методов классов
    __value = None

    # особенность JS: конструктор
    def __init__(self, value):
        self.__value = value
        self._next = None
    

    # ОСОБЕННОСТЬ JS: геттеры
    @property
    def value(self,):
        return self.__value
    


class LinkedList:
    __head = None
    __tail = None
    __size = 0

    def __init__(self, ):
        self.__head = None
        self.__tail = None
    

    def add(self, value):
        # ОСОБЕННОСТЬ JS: инкремент
        self.__size += 1

        if (not(self.__head)):
            self.__head = MyNode(value)
            self.__tail = self.__head
            return
        

        if (self.__head == self.__tail):
            self.__tail = MyNode(value)
            self.__head._next = self.__tail
            return
        

        currentNode = self.__head
        while (currentNode._next):
            currentNode = currentNode._next
        

        currentNode._next = MyNode(value)
        self.__tail = currentNode._next
    

    def __validateNotEmpty(self, ):
        if (not(self.__head)):
            # ОСОБЕННОСТЬ JS: исключения
            raise Exception("empty list")
        
    

    def __validateIndexInRange(self, index):
        if ((index < 0) or (index >= self.__size)):
            raise Exception("index out of range or index is not a positive integer")
        
    

    def remove(self, index):
        self.__validateNotEmpty()
        self.__validateIndexInRange(index)

        # особенность JS: декремент
        self.__size -= 1

        if (index == 0):
            self.__head = self.__head._next
            return
        

        currentNode = self.__head

        for i in range(0, index - 1, 1): 
            currentNode = currentNode._next
        

        currentNode._next = currentNode._next._next
    

