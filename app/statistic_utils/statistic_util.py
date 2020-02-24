""""
ProseRhythmDetector - the tool for extraction of rhythm features.
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
Утилита для подсчёта статистических характеристик для ритмических средств.
"""
import json
import re
import os
import traceback
from collections import OrderedDict

from textblob import TextBlob
import stanfordnlp

import pandas as pd
# from user_interface import get_arguments

from multiprocessing.dummy import Pool as ThreadPool

HELP_TEXT = """Usage: python3 statistic_utils/statistic_util.py -f FEATURES_DIR -o OUTPUT_FILE
-f FEATURES_DIR, --features=FEATURES_DIR:
\tPath to a directory with .prd.
-o OUTPUT_FILE, --output=OUTPUT_FILE:
\tThe output file.
-h, --help:
\tPrints help of the script.
"""


def generate_statistics(files, output_path, language):
    """
   входная точка в утилиту, которые формирует статискику для всех файлов

   Parameters:

   files: список файлов, подаваемых на вход утилите для дальнейшей обработки
   output_path: имя файла, где будет располагаться результат работы утилиты
   language: язык обрабатываемых текстов
   """
    open(output_path, 'w').close()

    # Итерируем список файлов и результат статистики пишем в качестве строки в файл
    file_result = []

    pool = ThreadPool(len(files))
    results = pool.starmap(generate_statistic, zip(files, [language for i in range(0, len(files))]))
    pool.close()
    pool.join()

    for result in results:
        try:
            result_list = []
            for f in ordered_features:
                if f == "top_words":
                    for i in range(0, 10):
                        result_list.append(result[f][i])
                else:
                    result_list.append(str(result[f]))
            file_result.append(result_list)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # задаём формат csv-файла
    table = pd.DataFrame(file_result, index=files,
                         columns=["anaphora",
                                  "epiphora",
                                  "symploce",
                                  "anadiplosis",
                                  "diacope",
                                  "epizeuxis",
                                  "epanalepsis",
                                  "gradual change",
                                  "chiasmus",
                                  "homogeneous members of the proposals",
                                  "polysyndeton",
                                  "sequence of exclamatory and interrogative sentences",
                                  "aposiopesis",
                                  "epistrophe",
                                  "one_word",
                                  "top1",
                                  "top2",
                                  "top3",
                                  "top4",
                                  "top5",
                                  "top6",
                                  "top7",
                                  "top8",
                                  "top9",
                                  "top10",
                                  "feat_per_sent",
                                  "NOUN",
                                  "ADJS",
                                  "VERB",
                                  "ADVB"])
    table.to_csv(output_path, header=True, index=True)


def generate_statistic(file, language):
    """
   генерация статистики для отдельного файла

   Parameters:

   file: файл для обработки
   language: язык обрабатываемого текста
   """
    print("Start preparing")
    f = open(file, encoding="utf-8")
    file_str = f.read()
    json_obj = json.loads(file_str)
    text = get_text(json_obj["text"])

    #  морфологический парсер
    # stanfordnlp.download(language)
    nlp = stanfordnlp.Pipeline(lang=language, processors='tokenize,mwt,pos')

    features = json_obj["features"]
    feature_dict = get_feature_dict()  # count of sentences with that feature
    words_dict = dict()  # key - word(feature), value - count of this word in text
    part_of_speech_dict = dict()  # словарь для частей речи

    # определение кол-ва предложений и слов в тексте
    blob = TextBlob(text)
    sentences_count = len(blob.sentences)
    words_in_text = blob.words

    splited_text = text.split()
    print("Finish preparing")
    print("Count of features: " + str(len(features)))
    i = 0
    for feature in features:
        sc = count_of_sentences_by_one_feature(feature, splited_text)  # кол-во предложений, ктр "задевает" фича
        feature_dict[feature["type"]] += sc
        for word in feature["words"]:  # просмотриваем список слов в фиче
            if 0 <= word < len(words_in_text):
                if words_in_text[word] in words_dict:  # 10 наиболее встречаемых слов...
                    words_dict[words_in_text[word]] += 1
                else:
                    words_dict[words_in_text[word]] = 1

                doc = nlp(words_in_text[word])
                PoS = doc.sentences[0].tokens[0].words[0].upos

                if PoS in ordered_part_of_speech:
                    if PoS in part_of_speech_dict:  # считаем части речи
                        part_of_speech_dict[PoS] += 1
                    else:
                        part_of_speech_dict[PoS] = 1
        i += 1
        if i % 500 == 0:
            print(str(i) + "-th iteration")

    for key in feature_dict:
        feature_dict[key] /= sentences_count

    #  добавляем части речи в feature_list
    for PoS in part_of_speech_dict:
        feature_dict[PoS] = part_of_speech_dict[PoS] / len(words_dict)

    # Доля слов, встречающихся 1 раз
    count = 0
    for key in words_dict:
        if words_dict[key] == 1:
            count += 1
    feature_dict["one_word"] = count / len(words_dict)
    feature_dict["feat_per_sent"] = len(features) / sentences_count

    # Добавляем топ 10 слов
    words_dict = OrderedDict(sorted(words_dict.items(), key=lambda x: x[1], reverse=True))
    feature_dict["top_words"] = []
    name = "top_words_" + os.path.basename(f.name)[:-4] + ".txt"
    with open(name, 'w', encoding="utf-8") as f:
        for key in list(words_dict.keys())[:10]:
            f.write(str(key) + " - " + str(words_dict[key]) + "\n")
            feature_dict["top_words"].append(words_dict[key])
    len_top_words = len(feature_dict["top_words"])
    if len_top_words < 10:
        for i in range(len_top_words, 10):
            feature_dict["top_words"].append("-")

    return feature_dict


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


def count_of_sentences_by_one_feature(feature, splited_text):
    """
   Получаем количество предложений, в которые входит указанная фича

   Parameters:
   feature: ритмическое средство (json-объект, у которого есть контекст, список слов, ...)
   splitted_text: текст, разбитый по пробелу
   """
    context = feature["context"]
    sub_string = " ".join(splited_text[context[0]: context[1]])
    regex = re.compile("[.|?|!] [A-Z|А-Я]")
    list_of_match = regex.findall(sub_string)
    len_list_if_match = len(list_of_match)
    if len_list_if_match == 0:
        return 1
    else:
        return len_list_if_match


ordered_features = (
    "anaphora",
    "epiphora",
    "symploce",
    "anadiplosis",
    "diacope",
    "epizeuxis",
    "epanalepsis",
    "gradual change",
    "chiasmus",
    "homogeneous members of the proposals",
    "polysyndeton",
    "sequence of exclamatory and interrogative sentences",
    "aposiopesis",
    "epistrophe",
    "one_word",
    "top_words",
    "feat_per_sent",
    "NOUN",
    "ADJ",
    "VERB",
    "ADV"
)

ordered_part_of_speech = (
    "NOUN",
    "ADJ",
    "VERB",
    "ADV"
)


def get_feature_dict():
    """
   Возвращаем стандартный словарь с фичами, где ключ - название фичи, значение - их количество

   """
    return {
        "anaphora": 0,
        "epiphora": 0,
        "symploce": 0,
        "anadiplosis": 0,
        "diacope": 0,
        "epizeuxis": 0,
        "epanalepsis": 0,
        "gradual change": 0,
        "chiasmus": 0,
        "homogeneous members of the proposals": 0,
        "polysyndeton": 0,
        "sequence of exclamatory and interrogative sentences": 0,
        "aposiopesis": 0,
        "epistrophe": 0,
        "NOUN": 0,
        "ADJ": 0,
        "VERB": 0,
        "ADV": 0
    }


if __name__ == "__main__":
    FEATURES_DIR, OUTPUT = get_arguments(HELP_TEXT)
    texts = []
    for filename in os.listdir(FEATURES_DIR):
        if filename.endswith('prd'):
            texts.append(os.path.join(FEATURES_DIR, filename))
    generate_statistics(texts, OUTPUT, 'en')
