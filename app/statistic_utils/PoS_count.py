"""
Утилита для подсчёта количества PoST.
"""
import traceback
import stanza
import sys
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

count = 0
complete = 0

# выбор языка
stanza.download('ru')
# stanza.download('es')
# stanza.download('en')
# stanza.download('fr')
nlp = stanza.Pipeline(lang='ru', processors='tokenize, pos')
sys.setrecursionlimit(2000)

PoST_list = [
    'ADJ',
    'ADP',
    'ADV',
    'AUX',
    'CCONJ',
    'DET',
    'INTJ',
    'NOUN',
    'NUM',
    'PART',
    'PRON',
    'PROPN',
    'SCONJ',
    'VERB',
]


def generate_statistics(files, PoS_count_res_file):
    """
   входная точка в утилиту, которая подсчитывает статистику PoST для всех файлов

   Parameters:

   files: список файлов, подаваемых на вход утилите для дальнейшей обработки
   PoS_count_res_file: имя файла, где будет располагаться результат работы утилиты
   """
    global count
    count = len(files)

    # очищаем файл перед новой записью
    open(PoS_count_res_file, 'w').close()

    # Итерируем список файлов и результат сохраняем
    # в список кортежей results [(имя файла (текста), словарь с результатом по данному тексту]), ... ]
    pool = ThreadPool(5)
    results = pool.starmap(generate_statistic, zip(files))
    pool.close()
    pool.join()

    # список значений, которые будут записаны в результатирующую csv-таблицу
    PoST_result = []

    for result in results:
        try:
            PoST_result.append(result[1].values())
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # результат записываем в csv-таблицу с именем PoS_count_res_file,
    # где столбцы - PoST, а строки - элементы из списка files
    table_PoS_count = pd.DataFrame(PoST_result, index=files, columns=PoST_list)
    table_PoS_count.to_csv(PoS_count_res_file, header=True, index=True)


def generate_statistic(file):
    """
    Функция для подсчёта статистики PoST для одного файла
    :param file: файл, переданные для обработки
    :return: кортеж вида (имя файла (текста), словарь с результатом по данному тексту])
    """
    global count, complete, nlp

    # создаем словарь, где ключи формируются из списка PoST_list, а значение по умолчанию - "0"
    PoST_dict = dict.fromkeys(PoST_list, 0)

    # считываем текст из файла
    text = get_text_file(file)

    """
    СТРУКТУРА ОТВЕТА STANZA
    
    stanza_text представляет собой json
     {
      "id": 11, номер слова в предложении, наверное :)
      "text": "wild",
      "upos": "ADJ",
      "xpos": "JJ",
      "feats": "Degree=Pos",
      "misc": "start_char=144159|end_char=144163"
    },
    """

    stanza_nlp = nlp(text)

    # формируем строку из upos на основе текста из файла
    stanza_text = [word.upos for sent in stanza_nlp.sentences for word in sent.words]

    # заполняем словарь PoST_dict
    for upos in stanza_text:
        if upos in PoST_dict.keys():
            PoST_dict[upos] += 1

    complete += 1
    print(complete, ' / ', count)

    return file, PoST_dict


def get_text_file(file):
    """
    Функция для считывания текста из файла
    :param file: файл, откуда считывается текст
    :return: текст ввиде строки, где абзацы соединены через пробел
    """
    f = open(file, encoding="utf-8")
    text = " ".join(f.read().split("\n"))
    return text


# список обрабатываемых файлов
names = open("", encoding="utf-8").read().split("\n")

files1 = names

generate_statistics(files1, 'PoS_count_res_file.csv')
