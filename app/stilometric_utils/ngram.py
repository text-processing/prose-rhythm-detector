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
import json
import traceback

from textblob import TextBlob
import pandas as pd

from multiprocessing.dummy import Pool as ThreadPool

HELP_TEXT = """Usage: python3 statistic_utils/statistic_util.py -f FEATURES_DIR -o OUTPUT_FILE
-f FEATURES_DIR, --features=FEATURES_DIR:
\tPath to a directory with .prd.
-o OUTPUT_FILE, --output=OUTPUT_FILE:
\tThe output file.
-h, --help:
\tPrints help of the script.
"""
count = 0
complete = 0


def generate_statistics(files, output_path_ngram1, output_path_ngram2, output_path_ngram3, output_path_ngram4):
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
    open(output_path_ngram1, 'w').close()
    open(output_path_ngram2, 'w').close()
    open(output_path_ngram3, 'w').close()
    open(output_path_ngram4, 'w').close()

    # Итерируем список файлов и результат статистики пишем в качестве строки в файл

    pool = ThreadPool(5)
    results = pool.starmap(generate_statistic, zip(files))
    pool.close()
    pool.join()

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

    for result in results:
        try:
            ngram1_result.append(take_file_ngram_result(ngram1_keys, result[1]))
            ngram2_result.append(take_file_ngram_result(ngram2_keys, result[2]))
            ngram3_result.append(take_file_ngram_result(ngram3_keys, result[3]))
            ngram4_result.append(take_file_ngram_result(ngram4_keys, result[4]))
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    table_ngram1 = pd.DataFrame(ngram1_result, index=files, columns=ngram1_keys)
    table_ngram1.to_csv(output_path_ngram1, header=True, index=True)

    table_ngram2 = pd.DataFrame(ngram2_result, index=files, columns=ngram2_keys)
    table_ngram2.to_csv(output_path_ngram2, header=True, index=True)

    table_ngram3 = pd.DataFrame(ngram3_result, index=files, columns=ngram3_keys)
    table_ngram3.to_csv(output_path_ngram3, header=True, index=True)

    table_ngram4 = pd.DataFrame(ngram4_result, index=files, columns=ngram4_keys)
    table_ngram4.to_csv(output_path_ngram4, header=True, index=True)


def generate_statistic(file):
    """
   генерация общей статистики для отдельного файла

   Parameters:

   file: файл для обработки
   """
    global count, complete

    print("Start")

    ngram1_dict = dict()
    ngram2_dict = dict()
    ngram3_dict = dict()
    ngram4_dict = dict()

    text = get_text_file(file)

    # создание отдельного объекта TextBlob без знаков пунктуации для подсчёта n-грамм
    STOP_PUNC = '– - — ! @ # $ % ^ & * ( ) + = _ ? № ; : " “ ” \' ’ « » ‘'.split()
    ngram1_text = ""
    for word in text:
        if word in STOP_PUNC:
            continue
        else:
            ngram1_text += word
    blob_ngram = TextBlob(ngram1_text)

    # определение n-грамм для конкретного текста
    get_ngram(blob_ngram, 1, ngram1_dict)
    get_ngram(blob_ngram, 2, ngram2_dict)
    get_ngram(blob_ngram, 3, ngram3_dict)
    get_ngram(blob_ngram, 4, ngram4_dict)

    ngram1_dict = sorted(ngram1_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram2_dict = sorted(ngram2_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram3_dict = sorted(ngram3_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]
    ngram4_dict = sorted(ngram4_dict.items(), key=lambda kv: kv[1], reverse=True)[:40]

    complete += 1
    print(complete, ' / ', count)

    return (file, ngram1_dict, ngram2_dict, ngram3_dict, ngram4_dict)


def get_text(text_list):
    """
   "Склеивает" json список слов в единый текст рекурсивно

   Parameters:

   text_list: список json-объектов под тегом text
   """
    text = ""
    for element in text_list:
        if type(element) is str:
            text += element + "\n"
        else:
            text += get_text(element)
    return text


def get_text_file(file):
    f = open(file, encoding="utf-8")
    file_str = f.read()
    json_obj = json.loads(file_str)
    text1 = get_text(json_obj["text"])
    text = " ".join(text1.split("\n"))
    return text


def get_ngram(blob, length, ngram_dict):
    """
    Функция для получение n-грамм заданной длинны 1 <= n <= 3 с учётом стоп-слов
    :param blob: объект textblob, содержащий в себе текст из обрабатываемого файла
    :param length: длинна n-граммы
    :param ngram_dict: словарь для записи n-грамм
    :return:
    """
    STOP_WORDS = 'I it my your his her its our their a the by for in on to в к с на о об обо во ко со по под за до над ' \
                 'от ото пред при у вне me us you him them this that - ! @ # $ % ^ & * ( ) + = _ — ? № ; : " “ ” \' ’ « » '.split()
    ngram = blob.ngrams(n=length)
    for gram in ngram:
        s_gram = gram.__getitem__(0)
        if s_gram in STOP_WORDS:
            continue
        str_gram = " ".join(gram)

        if str_gram in ngram_dict:
            ngram_dict[str_gram] += 1
        else:
            ngram_dict[str_gram] = 1


def expand_dict(original, other):
    for key, value in other:
        if key in original:
            original[key] += value
        else:
            original[key] = value


def take_file_ngram_result(ngram_list, ngram_dict):
    """
    Формируем список значений, соответствующий ngram_list (top-top-40),
    которые присутствуют в ngram_dict, то есть в top-40 для некоторого файла
    """
    result = []
    d = dict(ngram_dict)
    for n in ngram_list:
        if n in d:
            result.append(str(d[n]))
        else:
            result.append('0')
    return result

if __name__ == "__main__":
    FEATURES_DIR, OUTPUT = get_arguments(HELP_TEXT)
    texts = []
    for filename in os.listdir(FEATURES_DIR):
        if filename.endswith('prd'):
            texts.append(os.path.join(FEATURES_DIR, filename))
    generate_statistics(texts, OUTPUT)
