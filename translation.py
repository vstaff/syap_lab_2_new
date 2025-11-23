import re

# словарь шаблонов регулярных выражений под основные конструкции языка javascript
# объявления классов, методов, комментарии, объявление и инициализация полей классов и т.д.
REGEXES = dict(
    class_declaration=dict(
        regex=r"class \w+ \{\n",
        replacements=[
            (r' \{', r':', 1)
        ]
    ),
    commentary=dict(
        regex=r"\s*\/\/\s*[\wа-яА-Я;\s\\/.,:'\"!@#№$%^?&*()\-\+\=\[\]{}|<>]+\n",
        replacements=[
            (r'\/\/', '#', 1),
        ]
    ),

    constructor_declaration=dict(
        regex=r"\s*constructor\s*\([^)]*\)\s*\{\n",
        replacements=[
            (r'constructor\s*\(', r'def __init__(self, ', 1),
            (r'\)\s*\{', r'):', 1)
        ]
    ),

    class_private_property_declaration=dict(
        regex=r"\s*\#\w+ = \w+;?\n",
        replacements=[
            (r'#', '__', 1),
            (';', '', 1)
        ],
    ),

    class_private_property_init=dict(
        regex=r"\s*this\.#[\w_\.]+ = [\w\s_#\(\)\.]+;?\n",
        replacements=[
            ('this', 'self', 1),
            ('#', '__', 1),
            (';', '', 1),
        ]
    ),
    class_protected_property_init=dict(
        regex=r"\s*this\._\w+ = \w+;?\n",
        replacements=[
            ('this', 'self', 1),
            (';', '', 1)
        ]
    ),

    getter=dict(
        regex=r"\s*get \w+\(\) {\n",
        replacements=[
            ('get ', '@property\n  def ', 1),
            (r'\(', '(self,', 1),
            (r'\s*{\s*', ':\n', 1)
        ]
    ),

    return_=dict(
        regex=r"\s*return [\w.#]+;?\n",
        replacements=[
            (';', '', 1)
        ]
    ),

    class_property_init=dict(
        regex=r"\s*(this\.)?[#_]?[\w_.]+ = [\w_.]+;?\n",
        replacements=[
            ('this', 'self', 1),
            (';', '', 1),
        ]
    ),

    method_declaration=dict(
        regex=r"\s*[A-Za-z_][A-Za-z0-9_]*\s*\(\s*(?:[A-Za-z_][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*)?\s*\)\s*\{\n",
        replacements=[
            (r'\s\s', r'  def ', 1),
            # (r'def\s+.+(', r'def (self, ', 1),
            (r'\(', '(self, ', 1),
            (r'\s?{', ':', 1),
        ]
    ),

    private_method_declaration=dict(
        regex=r"\s*#[A-Za-z_][A-Za-z0-9_]*\s*\(\s*(?:[A-Za-z_][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*)?\s*\)\s*\{\n",
        replacements=[
            ('#', 'def __', 1),
            (r'\(', '(self, ', 1),
            (r'\s?{', ':', 1),
        ]
    ),

    # условия
    condition=dict(
        regex=r"\s*if\s*\(\s*[#A-Za-z0-9_+\-*/%<>=!&|?:.,'\"()[\]\s]*\)\s*\{\s*\n",
        replacements=[
            (r'!\s*\(', 'not(', 0),
            (r'\|\|', 'or', 0),
            ('&&', 'and', 0),
            (r'\s* {\s*\n', ':\n', 0),
            (r'===', '==', 0),
            (r'!==', '!=', 0)
        ]
    ),

    # исключения
    raising_exception=dict(
        regex=r"\s*throw new [\w\s\"\"_\(\)]+;?\n",
        replacements=[
            (r"throw new", "raise", 1)
        ]
    ),

    # инкремент, декремент (только постфиксные формы)
    increment_separate=dict(
        regex=r"\s*[\w_\.#]+\+\+;?\n?",
        replacements=[
            (r"\+\+", r" += 1", 1),
            (';', '', 0)
        ]
    ),
    decrement_separate=dict(
        regex=r"\s*[\w_\.#]+\-\-;?\n?",
        replacements=[
            (r"\-\-", r" -= 1", 1),
            (';', '', 0)
        ]
    ),

    # циклы
    while_loop=dict(
        regex=r'\s*while\s+\(?.+\)?\s+{\n',
        replacements=[
            (r'\s*{', ':', 1)
        ],
    ),

    # важно чтобы циклы for имели вид
    # for (let i = 0; i < ...; i++) {
    for_loop=dict(
        regex=r"\s*for\s*\(.*;.*;.*\)\s*{\n",
        replacements=[
            (r';', ',', 0),
            (r'for\s*\(', 'for i in range(', 1),
            (r'let\s+.+\s+=\s+', '', 1),
            (r',\s*.+\s*<\s*', ', ', 1),
            (r'.?\+\+', '1', 1),
            (r'\)', '):', 1)
        ]
    ),

    # теперь для второго скрипта
    # важно что при объявлении генераторов знак * должен стоять именно возле function
    function_declaration=dict(
        regex=r'function\*?',
        replacements=[
            (r'function\*?', 'def', 1),
            (r'\s*{', ':\n', 1)
        ]
    ),

    console_log=dict(
        regex=r'\s*console\.log',
        replacements=[
            (r'console\.log', 'print', 1),
        ]
    ),

    string_interpolation=dict(
        regex=r'.+`.+`',
        replacements=[
            (r'`', "f'", 1),
            (r'`', "'", 1),
        ]
    ),

    for_loop_in=dict(
        regex=r'\s*for\s*\((const|let)\s+.+\)\s*{\n',
        replacements=[
            (r'for\s*\((const|let)\s+', 'for ', 1),
            (r'\s+of\s+', ' in ', 1),
            (r'\)\s*{\n', ':\n', 1)
        ]
    ),
)

SMALL_PATCHES = [
    ("undefined", "None"),
    (r"this\.#", r"self.__"),
    (r"this\.", r"self."),

    (";", ""),
    ("let ", ""),
    ("Error", "Exception"),

    ("{\n", "\n"),
    ("}\n", "\n"),
    ("new ", ""),

    (r"  ", "    "),

    # скрипт 2
    ('const ', '')
]

# перевод типов из одного языка на другой
types_converter = dict(
    set=dict(
        js="Set",
        python="set",

        methods_attributes=dict(
            has="__contains__",
            size="__len__()",
        )
    ),

    array=dict(
        js=r"\[\]",
        python="[]",

        methods_attributes=dict(
            push="append",
        ),
    ),
)

# перевод обращения к различным библиотекам и их функциям
libs_converter = {
    "Math.random": "random.random",
    "Math.floor": "math.floor",
}

def translate(filename: str) -> None:
    lines: list[str] = []

    # хранит информацию о том, какой тип должен быть у переменной
    # после трансляции на питон
    types_storage = dict()

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # первичная трансляция - переводим крупные конструкции
    for i in range(len(lines)):
        line = lines[i]
        if line == '\n':
            continue

        for regex in REGEXES:
            if re.match(REGEXES[regex]['regex'], line):
                replacements = REGEXES[regex]['replacements']

                for replacement in replacements:
                    lines[i] = re.sub(replacement[0], replacement[1], lines[i], count=replacement[2])
                break
        # print(lines[i], end='')


    # вторичная трансляция - исправление мелких конструкций
    with open(f'./output/{filename}__OUTPUT.py', mode='w', encoding='utf-8') as output_file:
        for i in range(len(lines)):
            for pattern, replacement in SMALL_PATCHES:
                lines[i] = re.sub(pattern, replacement, lines[i])

            # промежуточный этап - преобразование типов между языками
            # для начала мы сохраняем в хранилище данных о типа переменных - тип переменной
            # одновременно (то есть в одном цикле происходят две вещи -
            # 1) переменные у которых объявлен тип - сохраняются в словарь (types_storage)
            #    точнее название самой переменной - и её тип
            # 2) ищутся строки в которых у переменных вызывается какой то метод, или атрибут; если
            #    ранее данные об этой переменной и её типе были сохранены - значит мы можем
            #    переименовать название метода или атрибута
            # UPD: также на этом этапе будет происходить трансляция обращений к различным библиотекам
            # js-библиотеки и обращения к ним будут заменены на python'вские
            for i in range(len(lines)):
                line = lines[i]
                new_data_in_types_storage = False

                for js_lib, python_lib in libs_converter.items():
                    # шаблон для регулярки - у какой-то библиотеки
                    # вызывается какая-то функция
                    lib_call_pattern = re.compile(
                        r'([A-Za-z_$][A-Za-z0-9_$]*)(\.)([A-Za-z_$][A-Za-z0-9_$]*)(\([^()]*\))?'
                    )
                    # если в текущей строке происходит обращение к функции
                    # из какой-то библиотеки
                    match_result = re.findall(lib_call_pattern, lines[i])
                    if match_result is None:
                        continue

                    for possible_lib_call in match_result:
                        possible_lib_call = ''.join(possible_lib_call).replace("(", "").replace(")", "")
                        if possible_lib_call in [*libs_converter.keys()]:
                            lines[i] = re.sub(possible_lib_call, libs_converter[possible_lib_call], lines[i])

                for tp in types_converter:
                    js_type_name = types_converter[tp].get("js")
                    py_type_name = types_converter[tp].get("python")

                    # шаблон инициализации переменной, принадлежащей к какому-то классу
                    pattern = r'\s*.+\s*=\s*' + js_type_name + r'(\(\))?'
                    # if re.match(fr'\s*.+\s*=\s*{js_type_name}\(\)', line):
                    if re.match(pattern, lines[i]):
                        split_parts = re.split(r"\s*=\s*", lines[i])
                        variable = split_parts[0].strip()
                        lines[i] = re.sub(js_type_name, py_type_name, lines[i])
                        # сохраняем переменную и её тип в хранилище
                        # делается это для того, чтобы потом можно
                        # было переименовать названия методов атрибутов класса
                        types_storage[variable] = tp
                        new_data_in_types_storage = True
                        break
                if new_data_in_types_storage:
                    continue
                # шаблон для регулярки - у какой-то переменной
                # вызывается метод или атрибут класса
                method_attribute_call_pattern = re.compile(
                    r'([A-Za-z_$][A-Za-z0-9_$]*)\.([A-Za-z_$][A-Za-z0-9_$]*)(\([^()]*\))?'
                )

                # если в текущей строке происходит обращение к методу или атрибуту класса
                # if method_attribute_call_pattern.match(lines[i]):
                match_result = re.search(method_attribute_call_pattern, lines[i])

                if match_result:
                    split_parts = match_result.group().split(".")
                    variable = split_parts[0].strip()
                    method_attribute = split_parts[1].strip()
                    method_attribute = re.sub(r'\(.+', '', method_attribute)
                    variables_in_storage = [*types_storage.keys()]
                    # print(lines[i])
                    if variable in variables_in_storage:
                        repl = types_converter[types_storage[variable]].get("methods_attributes").get(method_attribute) or method_attribute
                        lines[i] = re.sub(
                            method_attribute,
                            repl,
                            lines[i]
                        )

        output_file.writelines(lines)
    # print(types_storage)

def main():
    translate("./script_1.js")
    translate("./script_2.js")


if __name__ == '__main__':
    main()
