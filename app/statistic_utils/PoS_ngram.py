"""
Утилита для подсчёта статистики по PoST нграммам.
"""
import traceback
import stanza
import sys
from textblob import TextBlob
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import nltk

count = 0
complete = 0

nltk.download('punkt')

# выбор языка
stanza.download('ru')
# stanza.download('es')
# stanza.download('en')
# stanza.download('fr')
nlp = stanza.Pipeline(lang='ru', processors='tokenize, pos')
sys.setrecursionlimit(2000)


def generate_statistics(files, PoS_ngram1, PoS_ngram2, PoS_ngram3, PoS_ngram4):
    """
   входная точка в утилиту, которые формирует статискику для всех файлов

   Parameters:

   files: список файлов, подаваемых на вход утилите для дальнейшей обработки
   PoS_ngramN: имена файлов, где будут храниться результаты работы утилиты по конкретным n-граммам (N - кол-во слов в n-граммам)
   """
    global count
    count = len(files)

    # очищаем файлы перед новой записью
    open(PoS_ngram1, 'w').close()
    open(PoS_ngram2, 'w').close()
    open(PoS_ngram3, 'w').close()
    open(PoS_ngram4, 'w').close()

    # Итерируем список файлов и результат сохраняем
    # в список кортежей results [('file_name', [result[1]], [result[2]], [result[3]], [result[4]]), ...]
    pool = ThreadPool(5)
    results = pool.starmap(generate_statistic, zip(files))
    pool.close()
    pool.join()

    # общие словари для составления top-top-40
    ngram1_dict = dict()
    ngram2_dict = dict()
    ngram3_dict = dict()
    ngram4_dict = dict()

    for result in results:
        try:
            expand_dict(ngram1_dict, result[1])
            ngram1_dict = dict(sorted(ngram1_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])

            expand_dict(ngram2_dict, result[2])
            ngram2_dict = dict(sorted(ngram2_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])

            expand_dict(ngram3_dict, result[3])
            ngram3_dict = dict(sorted(ngram3_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])

            expand_dict(ngram4_dict, result[4])
            ngram4_dict = dict(sorted(ngram4_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    ngram1_keys = ngram1_dict.keys()
    ngram2_keys = ngram2_dict.keys()
    ngram3_keys = ngram3_dict.keys()
    ngram4_keys = ngram4_dict.keys()

    ngram1_result = []
    ngram2_result = []
    ngram3_result = []
    ngram4_result = []

    # получаем top-top-40 для нграмм того или иного размера (1, 2, 3 или 4 слова)

    # results = [('file_name', [result[1]], [result[2]], [result[3]], [result[4]]), ...]

    # result[1] = [('NOUN', 21), ('CCONJ', 7), ('VERB', 6), ('ADP', 5), ('PRON', 5), ('ADV', 2), ('DET', 1), ('ADJ', 1)]

    # result[2] = [('NOUN NOUN', 9), ('NOUN CCONJ', 6), ('CCONJ NOUN', 5), ('PRON VERB', 4), ('ADP NOUN', 3),
    # ('NOUN ADP', 3), ('NOUN PRON', 2), ('VERB NOUN', 2), ('ADP DET', 1), ('DET ADJ', 1), ('ADJ NOUN', 1),
    # ('VERB VERB', 1), ('VERB CCONJ', 1), ('CCONJ VERB', 1), ('VERB PRON', 1), ('VERB ADP', 1), ('ADP PRON', 1),
    # ('PRON NOUN', 1), ('CCONJ ADV', 1), ('ADV ADV', 1), ('ADV PRON', 1)]

    # result[3], result[4] аналогично
    for result in results:
        try:
            ngram1_result.append(take_file_ngram_result(ngram1_keys, result[1]))
            ngram2_result.append(take_file_ngram_result(ngram2_keys, result[2]))
            ngram3_result.append(take_file_ngram_result(ngram3_keys, result[3]))
            ngram4_result.append(take_file_ngram_result(ngram4_keys, result[4]))
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # результат записываем в csv-таблицы с именем PoS_ngramN,
    # где столбцы - top-top-40 нграмм того или иного размера (1, 2, 3 или 4 слова), а строки - элементы из списка files
    table_ngram1 = pd.DataFrame(ngram1_result, index=files, columns=ngram1_keys)
    table_ngram1.to_csv(PoS_ngram1, header=True, index=True)

    table_ngram2 = pd.DataFrame(ngram2_result, index=files, columns=ngram2_keys)
    table_ngram2.to_csv(PoS_ngram2, header=True, index=True)

    table_ngram3 = pd.DataFrame(ngram3_result, index=files, columns=ngram3_keys)
    table_ngram3.to_csv(PoS_ngram3, header=True, index=True)

    table_ngram4 = pd.DataFrame(ngram4_result, index=files, columns=ngram4_keys)
    table_ngram4.to_csv(PoS_ngram4, header=True, index=True)


def generate_statistic(file):
    """
       Функция для подсчёта статистики PoST нграмм для одного файла
       :param file: файл, переданные для обработки
       :return: кортеж вида ('file_name', [result[1]], [result[2]], [result[3]], [result[4]])
       """
    global count, complete, nlp

    # словари нграмм для конкретного файла
    ngram1_dict = dict()
    ngram2_dict = dict()
    ngram3_dict = dict()
    ngram4_dict = dict()

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

    # формируем строку из upos на основе текста из файла.
    # Если upos содержится в списке ["PUNCT", "SYM", "X"], то элемент не записывается в результатирующую строку
    stanza_text = " ".join(
        [word.upos for sent in stanza_nlp.sentences for word in sent.words if word.upos not in ["PUNCT", "SYM", "X"]])

    blob_ngram = TextBlob(stanza_text)

    # определение n-грамм для конкретного текста с записью их в ngramN_dict
    get_ngram(blob_ngram, 1, ngram1_dict)
    get_ngram(blob_ngram, 2, ngram2_dict)
    get_ngram(blob_ngram, 3, ngram3_dict)
    get_ngram(blob_ngram, 4, ngram4_dict)

    # словари с нграммами превращаются в списки кортежей вида:

    # ngram1_dict = [('NOUN', 21), ('CCONJ', 7), ('VERB', 6), ('ADP', 5), ('PRON', 5), ('ADV', 2), ('DET', 1), ('ADJ', 1)]

    # [('NOUN NOUN', 9), ('NOUN CCONJ', 6), ('CCONJ NOUN', 5), ('PRON VERB', 4), ('ADP NOUN', 3), ('NOUN ADP', 3),
    #  ('NOUN PRON', 2), ('VERB NOUN', 2), ('ADP DET', 1), ('DET ADJ', 1), ('ADJ NOUN', 1), ('VERB VERB', 1),
    #  ('VERB CCONJ', 1), ('CCONJ VERB', 1), ('VERB PRON', 1), ('VERB ADP', 1), ('ADP PRON', 1), ('PRON NOUN', 1),
    #  ('CCONJ ADV', 1), ('ADV ADV', 1), ('ADV PRON', 1)]

    ngram1_list = sorted(ngram1_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram2_list = sorted(ngram2_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram3_list = sorted(ngram3_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram4_list = sorted(ngram4_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]

    complete += 1
    print(complete, ' / ', count)

    return file, ngram1_list, ngram2_list, ngram3_list, ngram4_list


def get_text_file(file):
    """
    Функция для считывания текста из файла
    :param file: файл, откуда считывается текст
    :return: текст ввиде строки, где абзацы соединены через пробел
    """
    f = open(file, encoding="utf-8")
    text = " ".join(f.read().split("\n"))
    return text


def get_ngram(blob, length, ngram_dict):
    """
    Функция для получение n-грамм заданной длинны 1 <= n <= 4
    :param blob: объект textblob, содержащий в себе текст из обрабатываемого файла
    :param length: длинна n-граммы
    :param ngram_dict: словарь для записи n-грамм
    :return: None
    """
    ngram = blob.ngrams(n=length)
    for gram in ngram:
        str_gram = " ".join(gram)

        if str_gram in ngram_dict:
            ngram_dict[str_gram] += 1
        else:
            ngram_dict[str_gram] = 1


def expand_dict(original, other):
    """
    Функция дополняет словарь original элементами из списка кортежей other
    :param original: исходный словарь для дополнения
    :param other: список кортежей вида [(key, value), ...]
    :return: None
    """
    for key, value in other:
        if key in original:
            original[key] += value
        else:
            original[key] = value


def take_file_ngram_result(ngram_keys, ngram_list):
    """
    Функция формирует список значений, соответствующий top-top-40,
    (top-40 среди top-40 для каждого файла)
    :param ngram_keys:
    :param ngram_list:
    :return:
    """
    result = []
    d = dict(ngram_list)
    for n in ngram_keys:
        if n in d:
            result.append(str(d[n] / sum(d.values())))
        else:
            result.append('0')
    return result


# список обрабатываемых файлов
names = open("", encoding="utf-8").read().split("\n")

files1 = names

generate_statistics(files1, 'PoS_ngram1_pt1.csv', 'PoS_ngram2_pt1.csv', 'PoS_ngram3_pt1.csv', 'PoS_ngram4_pt1.csv')
