""""
ProseRhythmDetector - the tool for extraction of rhythm features and computation of stylometric features for texts.
    Copyright (C) 2020  Vladislav Larionov, Vladislav Petryakov, Anatoly Poletaev, Ksenia Lagutina, Alla Manakhova, Nadezhda Lagutina, Elena Boychuk.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
    The corresponding author: Ksenia Lagutina, lagutinakv@mail.ru
"""

"""
Утилита для подсчёта статистики по н-граммам.
"""
import traceback
from textblob import TextBlob
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import re

count = 0
complete = 0


def generate_statistics(files, output_path_ngram1, output_path_ngram2, output_path_ngram3):
    """
   входная точка в утилиту, которые формирует статискику для всех файлов

   Parameters:

   files: список файлов, подаваемых на вход утилите для дальнейшей обработки
   output_path_general: имя файла, где будет располагаться результат работы утилиты по общим характеристикам
   output_path_ngramN: имена файлов, где будут храниться результаты работы утилиты по конкретным n-граммам (N - кол-во слов в n-граммам)
   language: язык обрабатываемых текстов
   """
    global count
    count = len(files)

    # очищаем файлы перед новой записью
    open(output_path_ngram1, mode='w').close()
    open(output_path_ngram2, mode='w').close()
    open(output_path_ngram3, mode='w').close()

    # Итерируем список файлов и результат статистики пишем в качестве строки в файл
    # в список кортежей results [('file_name', [result[1]], [result[2]], [result[3]]), ...]
    pool = ThreadPool(5)
    results = pool.starmap(generate_statistic, zip(files))
    pool.close()
    pool.join()

    # общие словари для составления top-top-40
    ngram1_dict = dict()
    ngram2_dict = dict()
    ngram3_dict = dict()

    for result in results:
        try:
            expand_dict(ngram1_dict, result[1])
            ngram1_dict = dict(sorted(ngram1_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])

            expand_dict(ngram2_dict, result[2])
            ngram2_dict = dict(sorted(ngram2_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])

            expand_dict(ngram3_dict, result[3])
            ngram3_dict = dict(sorted(ngram3_dict.items(), key=lambda kv: kv[1], reverse=True)[:40])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    ngram1_keys = ngram1_dict.keys()
    ngram2_keys = ngram2_dict.keys()
    ngram3_keys = ngram3_dict.keys()

    ngram1_result = []
    ngram2_result = []
    ngram3_result = []

    # получаем top-top-40 для нграмм того или иного размера (1, 2 или 3 слова)
    # results = [('file_name', [result[1]], [result[2]], [result[3]]), ...]
    for result in results:
        try:
            ngram1_result.append(take_file_ngram_result(ngram1_keys, result[1]))
            ngram2_result.append(take_file_ngram_result(ngram2_keys, result[2]))
            ngram3_result.append(take_file_ngram_result(ngram3_keys, result[3]))
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # результат записываем в csv-таблицы с именем output_path_ngramN,
    # где столбцы - top-top-40 нграмм того или иного размера (1, 2 или 3 слова), а строки - элементы из списка files
    table_ngram1 = pd.DataFrame(ngram1_result, index=files, columns=ngram1_keys)
    table_ngram1.to_csv(output_path_ngram1, header=True, index=True)

    table_ngram2 = pd.DataFrame(ngram2_result, index=files, columns=ngram2_keys)
    table_ngram2.to_csv(output_path_ngram2, header=True, index=True)

    table_ngram3 = pd.DataFrame(ngram3_result, index=files, columns=ngram3_keys)
    table_ngram3.to_csv(output_path_ngram3, header=True, index=True)


def generate_statistic(file):
    """
    Функция для подсчёта статистики PoST нграмм для одного файла
    :param file: файл, переданные для обработки
    :return: кортеж вида ('file_name', [result[1]], [result[2]], [result[3]]])
    """
    global count, complete

    # словари нграмм для конкретного файла
    ngram1_dict = dict()
    ngram2_dict = dict()
    ngram3_dict = dict()

    # считываем текст из файла
    text = re.sub(r'[^\w\s]', '', get_text_file(file)).lower()
    blob_ngram = TextBlob(text)

    # определение n-грамм для конкретного текста с записью их в ngramN_dict
    get_ngram(blob_ngram, 1, ngram1_dict)
    get_ngram(blob_ngram, 2, ngram2_dict)
    get_ngram(blob_ngram, 3, ngram3_dict)

    # словари с нграммами превращаются в списки кортежей вида:
    # ngram1_dict = [('NOUN', 21), ('CCONJ', 7), ('VERB', 6), ('ADP', 5), ('PRON', 5), ('ADV', 2), ('DET', 1), ('ADJ', 1)]
    ngram1_dict = sorted(ngram1_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram2_dict = sorted(ngram2_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram3_dict = sorted(ngram3_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]

    complete += 1
    print(complete, ' / ', count)

    return file, ngram1_dict, ngram2_dict, ngram3_dict


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
    Функция для получение n-грамм заданной длинны 1 <= n <= 3 с учётом стоп-слов
    :param blob: объект textblob, содержащий в себе текст из обрабатываемого файла
    :param length: длинна n-граммы
    :param ngram_dict: словарь для записи n-грамм
    :return: None
    """

    ngram = blob.ngrams(n=length)
    for gram in ngram:
        str_gram = " ".join(gram).replace("'", "")

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


def take_file_ngram_result(ngram_keys, ngram_dict):
    """
    Функция формирует список значений, соответствующий top-top-40,
    (top-40 среди top-40 для каждого файла)
    :param ngram_keys:
    :param ngram_list:
    :return:
    """
    result = []
    d = dict(ngram_dict)
    for n in ngram_keys:
        if n in d:
            result.append(str(d[n] / sum(d.values())))
        else:
            result.append('0')
    return result


names = open("", encoding="utf-8").read().split("\n")

files1 = names

output_path_ngram1 = ""
output_path_ngram2 = ""
output_path_ngram3 = ""

generate_statistics(files1, output_path_ngram1, output_path_ngram2, output_path_ngram3)
