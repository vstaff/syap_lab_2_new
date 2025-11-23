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
    )
)

SMALL_PATCHES = [
    ("undefined", "None"),
    (r"this\.#", r"self.__"),
    (r"this\.", r"self."),

    (";", ""),
    ("let ", ""),
    ("Error", "Exception"),

    ("{", ""),
    ("}", ""),
    ("new ", ""),

    (r"  ", "    "),
]

def translate(filename: str) -> None:
    lines: list[str] = []
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

        output_file.writelines(lines)

def main():
    translate("./script_1.js")


if __name__ == '__main__':
    main()
