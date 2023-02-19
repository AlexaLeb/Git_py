import random as r
from pprint import pprint

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
    """
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
    число 11, чтобы перейти к чтению следующего вопроса.
    В конце функция перемешивает вопросы, чтобы в будущем те шли  у людей в рандомном порядке
    :param file_path:
    :returnsw as:
    """
    file = open(file_path, 'r',)
    dictionaries = []
    text = []
    for line in file.read().splitlines():
        text.append(line)
    i = 0
    while i < len(text):
        dictionary = {}
        dictionary['number'] = text[i]
        dictionary['type'] = text[i+1]
        dictionary['question'] = text[i+2]
        dictionary['variants'] = [text[i+3], text[i+4], text[i+5], text[i+6]]
        dictionary['answer'] = text[i+7]
        dictionary['score'] = text[i+8]
        dictionary['tries'] = text[i+9]
        dictionaries.append(dictionary)
        i += 11
    r.shuffle(dictionaries)
    return dictionaries

def questioner(dictionaries):
    player_score = 0
    overall = {}
    print(Color.BLUE + Color.BOLD + 'Добро пожаловать в нашу викторину по Python! Хочешь принять учаситие и опробовать свои силы?')
    while True:
        welcome = input(Color.BLUE + Color.BOLD + 'Напиши "да" или "нет" ' + Color.END)
        if welcome.lower() == 'да':
            break
        else:
            print(Color.BLUE + Color.BOLD + r.choice(['Может все-таки поучавствуешь?', 'Мы же старались(((', 'Подумай еще', 'Приходи, когда передумаешь' + Color.END]))
    player_name = input(Color.BOLD + 'Добро пожаловать в нашу викторину по Python! Пожалуйства, введите ваше имя: ' + Color.END)
    overall['name'] = player_name
    counter = 0
    for question in dictionaries:
        ask = asker(question)
        player_score += ask[0]
        answer = ask[1]
        counter += 1
        dict_with_aswr = {
            'question': question['variants'],
            'answer of player': answer,
            'right answer': question['answer']
        }
        overall[f'question number {counter}'] = dict_with_aswr
    overall['overall score'] = player_score
    return f'Викторина окончена', overall

def asker(question):
    score = int(question['score'])
    tries = int(question['tries'])
    question_printer(question)
    while True:
        answer = input(Color.DARKCYAN + 'Ваш ответ: ' + Color.END)
        if set(answer) == set(question['answer']):
            print(Color.GREEN + 'Поздравляю, вы абсолютно правы!' + Color.END)
            return score, answer
        elif tries == 1:
            print(Color.RED + Color.BOLD + f'К сожалению, вы так и не дали правильного ответа.\nВаши попытки кончились.' + Color.END)
            return 0, answer
        else:
            tries -= 1
            print(Color.YELLOW + 'Вы неправы' + Color.RED + '!!!' + Color.END, f'\nПопробуйте еще раз')
            question_printer(question)
            score -= 1

def question_printer(question):
    print(Color.DARKCYAN + Color.UNDERLINE + Color.BOLD + question['question'] + Color.END)
    if question['type'] == 'S':
        print(Color.DARKCYAN + 'Вопрос с одним вариантом ответа:' + Color.END)
    else:
        print(Color.DARKCYAN + 'Доступно несколько вариантов ответа:' + Color.END)
    for parts in question['variants']:
        print(parts)
    return True


# pprint(file_reader('questions.txt'))
print(questioner(file_reader('questions.txt')))