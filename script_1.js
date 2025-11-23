class MyNode {
  // ОСОБЕННОСТЬ JS: реализаций приватных свойств и методов классов
  #value = undefined;

  // особенность JS: конструктор
  constructor(value) {
    this.#value = value;
    this._next = undefined;
  }

  // ОСОБЕННОСТЬ JS: геттеры
  get value() {
    return this.#value;
  }
}

class LinkedList {
  #head = undefined;
  #tail = undefined;
  #size = 0;

  constructor() {
    this.#head = undefined;
    this.#tail = undefined;
  }

  add(value) {
    // ОСОБЕННОСТЬ JS: инкремент
    this.#size++;

    if (!(this.#head)) {
      this.#head = new MyNode(value);
      this.#tail = this.#head;
      return;
    }

    if (this.#head === this.#tail) {
      this.#tail = new MyNode(value);
      this.#head._next = this.#tail;
      return;
    }

    let currentNode = this.#head;
    while (currentNode._next) {
      currentNode = currentNode._next;
    }

    currentNode._next = new MyNode(value);
    this.#tail = currentNode._next;
  }

  #validateNotEmpty() {
    if (!(this.#head)) {
      // ОСОБЕННОСТЬ JS: исключения
      throw new Error("empty list");
    }
  }

  #validateIndexInRange(index) {
    if ((index < 0) || (index >= this.#size)) {
      throw new Error("index out of range or index is not a positive integer");
    }
  }

  remove(index) {
    this.#validateNotEmpty();
    this.#validateIndexInRange(index);

    // особенность JS: декремент
    this.#size--;

    if (index == 0) {
      this.#head = this.#head._next;
      return;
    }

    let currentNode = this.#head;

    for (let i = 0; i < index - 1; i++) {
      currentNode = currentNode._next;
    }

    currentNode._next = currentNode._next._next;
  }
}