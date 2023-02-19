class Color:
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def file_reader(file_path) -> list:
    '''
    Функция принимает в качестве параметра путь к файлу с вопросами. Важно, чтобы вопросы в файле были оформлены
    определенным образом. На выходе функция выдает список словарей, каждый словарь имеет ключи:
    - номер вопроса
    - тип вопроса
    - вопрос из 5 строчек
    - правильный ответ
    - баллы за вопрос
    - количество попыток при ответе на вопрос
    Алгоритм построен так, что после преобразования файла в список начинает читать его по индексу i+n, где n -
    добавочное число для более легкого добавления в словрь, после того, как добавлены все значеня словаря к i добавляется
    число 11, чтобы перейти к чтению следующего вопроса
    :param file_path:
    :return: list
    '''
    file = (open(file_path, 'r',))
    dictionaries = []
    text = []
    for line in file.read().splitlines():
        text.append(line.split('\n'))
    i = 0
    while i < len(text):
        dictionary = {}
        dictionary['number'] = text[i]
        dictionary['type'] = text[i+1]
        dictionary['question'] = [text[i+2], text[i+3], text[i+4], text[i+5], text[i+6]]
        dictionary['correct answer'] = text[i+7]
        dictionary['score'] = text[i+8]
        dictionary['tries'] = text[i+9]
        dictionaries.append(dictionary)
        i += 11
    return dictionaries


print(file_reader('questions.txt'))
