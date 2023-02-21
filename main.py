import random as r
"""
Описание Дани
"""


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
    добавочное число для более легкого добавления в словарь, после того, как добавлены все значения словаря к i добавляется
    число 11, чтобы перейти к чтению следующего вопроса.
    В конце функция перемешивает вопросы, чтобы в будущем те шли у людей в случайном порядке.
    :param file_path:
    :return dictionaries:
    """
    dictionaries = []  # Список в который в будущем будут добавляться словари вопросов.
    text = []  # Список в который будет записываться информация из словаря.
    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file.read().splitlines():
            text.append(line)  # Каждая строчка из файла становится отдельным элементом списка.
        file.close()
    for question_string_step in range(0, len(text), 11):  # 11 - длина каждого вопроса в строчках с учетом текста, типа
        # вопроса, ответа, номера, баллов попыток и пустой строки, которая нужна для читабельности файла с вопросами
        dictionary = {  # Словарь вопроса, в каждый ключ записывается значение из списка. Так как список структурирован,
            # то нужные значения всегда попадают к нужным ключам
            'number': text[question_string_step],
            'type': text[question_string_step + 1],
            'question': text[question_string_step + 2],
            'variants': [text[question_string_step + 3], text[question_string_step + 4], text[question_string_step + 5],
                         text[question_string_step + 6]],
            'answer': text[question_string_step + 7],
            'score': text[question_string_step + 8],
            'tries': text[question_string_step + 9]
        }
        dictionaries.append(dictionary)
    r.shuffle(dictionaries)  # Вопросы в списке перемешиваются, поэтому каждый раз они идут в новом порядке
    return dictionaries


def questioner(dictionaries: list):
    """
    Основная функция кода, с нее начинается работа программы. В начале она задает несколько переменных - имя игрока,
    максимальный балл за викторину. Функция здоровается с игроком и начинает викторину. Она перебирает все вопросы, для
    каждого вызывая asker - функцию задания вопросов. Ответ пользователя, балл за вопрос, и максимальный бал за вопрос,
    текст вопроса функция записывает в словарь, который получает порядковый номер вопроса. Каждый из новых словарей
    попадает словарь overall, который содержит все вопросы, имя пользователя, его итоговый результат, максимально
    возможный результат и количество вопросов. Когда вопросы кончаются она комментирует результат игрока и выводит его.
    В конце код вызывает функцию для записи результатов в файл.
    :param dictionaries:
    :return:
    """
    player_score = 0  # Переменная с количеством баллов у игрока
    max_score = 0  # Максимум баллов за вопросы игрока
    print(Color.BLUE + Color.BOLD + 'Добро пожаловать в нашу викторину по Python! Хочешь принять участие и опробовать свои силы?')
    while True:  # Цикл, который не прервется, пока пользователь не решит пройти викторину
        welcome = input(Color.BLUE + Color.BOLD + 'Напиши "да" или "нет" ' + Color.END)
        if welcome.lower() == 'да' or welcome.lower() == 'yes':  # Когда код получает согласие викторина начинается
            break
        else:  # Если пользователь не дал согласие на начало, код будет выдавать 4 реплики-просьбы начать в случайном порядке
            print(Color.BLUE + Color.BOLD + r.choice(['Может все-таки поучаствуешь?', 'Мы же старались(((',
                                                      'Подумай еще', 'Приходи, когда передумаешь' + Color.END]))
    player_name = input(Color.BOLD + 'Пожалуйста, введите ваше имя: ' + Color.END)  # Игрок вводит имя
    overall = {
        'name': player_name
    }
    counter = 0  # Переменная необходимая, для создания порядкового номера вопроса. Нужно для нумерации вопросов.
    for question in dictionaries:  # Перебирает вопросы в списке вопросов. Каждый вопрос - словарь
        ask = asker(question)  # Вызывает функцию задавания вопросов. Ask - кортеж, который содержит счет игрока и ответ
        player_score += ask[0]
        max_score += int(question['score'])
        counter += 1
        answer_dict = {
            'question': question['question'],
            'variants': question['variants'],
            'answer of player': ask[1],
            'right answer': question['answer'],
            'score': ask[0]
        }
        overall[f'question number {counter}'] = answer_dict  # Словарь вопроса записывается в итоговый словарь,
        # получая порядковое имя.
    overall['name'] = player_name
    overall['overall score'] = str(player_score)
    overall['question amount'] = counter
    overall['max_score'] = str(max_score)
    print(Color.BOLD + '\nИтог:' + Color.END)
    if player_score == max_score:  # Если ответ максимальный, то код хвалит игрока.
        print(Color.GREEN + 'Молодец, отличный результат!' + Color.END)
        overall['commentary'] = 'Молодец, отличный результат!'
    elif player_score > max_score/2:  # Если правильно больше половины, то код нейтрально отзывается об игроке.
        print(Color.YELLOW + 'Нуууу, экзамен ты на "зачет" сдашь' + Color.END)
        overall['commentary'] = 'Нуууу, экзамен ты на "зачет" сдашь'
    else:  # Если меньше половины решено, то код просит игрока идти учиться.
        print(Color.RED + 'Беги готовиться! ТЫ ничего не знаешь' + Color.END)
        overall['commentary'] = 'Беги готовиться! ТЫ ничего не знаешь'
    print('Ты набрал', Color.UNDERLINE + Color.DARKCYAN + str(player_score) + Color.END, 'баллов из', Color.BOLD +
          Color.DARKCYAN + str(max_score) + Color.END)
    writer(overall)  # Вызов функции для записи в файл
    return f'Викторина окончена'


def asker(question: dict) -> tuple:
    """
    Функция принимает словарь с вопросом и читает его. Для вывода вопроса она вызывает функцию question_printer.
    В переменной answer пользователь записывает ответ, если ответ верный, то пользователь получает максимум баллов, если
    же ответ пользователя не равен правильному ответу, то функция будет предлагать ему ответить еще раз, пока у него не
    кончатся попытки ответа на этот вопрос. С каждой попыткой у пользователя отнимают один балл на вопрос, если попытки
    кончились, то пользователь получает 0 баллов. Функция возвращает кортеж с балами и ответом игрока.
    :param question:
    :return score, answer:
    """
    score = int(question['score'])  # Максимальное количество баллов за вопрос
    tries = int(question['tries'])  # Количество попыток ответа на этот вопрос
    question_printer(question)  # Здесь вызывается функция, которая печатает вопрос.
    while True:
        answer = input(Color.DARKCYAN + 'Ваш ответ: ' + Color.END)  # Пользователь записывает свой ответ сюда.
        if set(answer) == set(question['answer']):  # Сравнивается ответ пользователя и ответ правильный.
            # Ответ пользователя и правильный превращены в множество set, чтобы в ответах на вопрос с несколькими
            # вариантами код засчитал любую правильную комбинацию цифр ответа.
            print(Color.GREEN + 'Поздравляю, вы абсолютно правы!' + Color.END)
            return score, answer
        elif tries == 1:  # Количество попыток доходит до этого значения, то пользователь так и не дал правильный ответ
            print(Color.RED + Color.BOLD + f'К сожалению, вы так и не дали правильного ответа.\nВаши попытки кончились.' + Color.END)
            return 0, answer
        else:  # Ответ был не правильный, код дает пользователю еще шанс, но наказывает снятием баллов
            tries -= 1  # Количество попыток уменьшается
            score -= 1  # За неправильный ответ снижается максимально возможный балл за ответ
            print(Color.YELLOW + 'Вы неправы' + Color.RED + '!!!' + Color.END, f'\nПопробуйте еще раз')
            question_printer(question)  # Здесь вызывается функция, которая печатает вопрос.


def question_printer(question: dict):
    """
    Функция принимает словарь с вопросом, находит вопрос, определяет его тип (один вариант или больше) вопроса, находит
    варианты и печатает все это.
    :param question:
    :return None:
    """
    print()  # Пустая строчка для того, чтобы вопрос визуально отделялся от текста выше.
    print(Color.DARKCYAN + Color.UNDERLINE + Color.BOLD + question['question'] + Color.END)
    if question['type'] == 'S':  # S - singular, означает, что вопрос имеет один правильный ответ
        print(Color.DARKCYAN + 'Вопрос с одним вариантом ответа:' + Color.END)
    else:  # Вопрос имеет более одного правильного ответа. В файле они помечены M, но код отнесет сюда все вопросы без S
        print(Color.DARKCYAN + 'Возможно несколько правильных вариантов ответа:' + Color.END)
    for parts in question['variants']:  # Печатает варианты ответа
        print(parts)


def writer(dictionary: dict):
    """
    Функция записывает значения в файл. Имя файла - имя пользователя. Весь код функция просто упорядоченно печатает
    информацию из словаря, который она получила на входе. Словарь должен быть строго структурирован.
    :param dictionary:
    :return:
    """
    with open(dictionary['name'] + '.txt', 'w', encoding='UTF-8') as file:  # Для имени файла используется имя игрока
        print('Викторину прошел -', dictionary['name'], file=file)
        for question_id in range(1, int(dictionary['question amount'] + 1)):  # Цикл для обработки каждого вопроса
            print(f'Вопрос номер {question_id}', file=file)
            question = dictionary[f'question number {question_id}']  # переменная, которая обращается к словарю с
            # вопросом в словаре итоговом
            print(question['question'], file=file)
            for text_id in range(0, len(question['variants'])):
                print(question['variants'][text_id], file=file)
            print('Ваш ответ:', question['answer of player'], file=file)
            if set(question['answer of player']) == set(question['right answer']):  # С множествами сравнивает ответы
                print('Ваш ответ верный!', file=file)
            else:
                print('Ваш ответ неверный!', file=file)
            print('Правильный ответ:', question['right answer'], 'За этот вопрос вы получаете', question['score'], 'балла(ов)', file=file)
        print('Итог:', file=file)
        print(dictionary['commentary'], f'Ты набрал {dictionary["overall score"]} баллов из {dictionary["max_score"]}', file=file)
    file.close()


questioner(file_reader('questions.txt'))
