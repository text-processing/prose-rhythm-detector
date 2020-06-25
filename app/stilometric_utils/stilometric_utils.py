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
Утилита для подсчёта статистики для стилометрических характеристик.
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

ordered_features = [
    "number_of_alphabets",
    "number_of_characters",
    "number_of_words",
    "number_of_sentence",
    "average_sentence_length_by_character",
    "average_sentence_length_by_word",
    "average_word_length"
]

ordered_features_az_punc = [
    # "a",
    # "b",
    # "c",
    # "d",
    # "e",
    # "f",
    # "g",
    # "h",
    # "i",
    # "j",
    # "k",
    # "l",
    # "m",
    # "n",
    # "o",
    # "p",
    # "q",
    # "r",
    # "s",
    # "t",
    # "u",
    # "v",
    # "w",
    # "x",
    # "y",
    # "z",
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ё",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
    # "ç",
    # "à",
    # "â",
    # "é",
    # "è",
    # "ê",
    # "ë",
    # 'î',
    # "ï",
    # "ô",
    # "ù",
    # "û",
    # "ü",
    # "ÿ",
    ".",
    ",",
    "!",
    "@",
    "\'",
    "#",
    "№",
    "\"",
    ";",
    "$",
    "%",
    "^",
    ":",
    "&",
    "?",
    "*",
    ")",
    "(",
    "_",
    "–",
    "-",
    "—"
]

count = 0
complete = 0


def generate_statistics(files, output_path_general, output_path_letters_punc):
    """
   входная точка в утилиту, которые формирует статискику для всех файлов

   Parameters:

   files: список файлов, подаваемых на вход утилите для дальнейшей обработки
   output_path_general: имя файла, где будет располагаться результат работы утилиты по общим характеристикам
   output_path_letters_punc: имя файла, где будет распологаться результат работы утилиты по отдельным буквам и знакам
   """

    global count
    count = len(files)

    open(output_path_general, 'w').close()
    open(output_path_letters_punc, 'w').close()

    # Итерируем список файлов и результат статистики пишем в качестве строки в файл

    pool = ThreadPool(5)
    results = pool.starmap(generate_statistic, zip(files))
    results_az_punc = pool.starmap(generate_statistic_az_punc, zip(files))
    pool.close()
    pool.join()

    file_result = []
    file_result_az_punc = []

    for result in results_az_punc:
        try:
            file_result_az_punc.append(result)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    for result in results:
        try:
            result_list = []
            for f in ordered_features:
                result_list.append(str(result[f]))
            file_result.append(result_list)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # задаём формат csv-файла для статистики по общим характеристикам
    table_general = pd.DataFrame(file_result, index=files,
                                 columns=["number_of_alphabets",
                                          "number_of_characters",
                                          "number_of_words",
                                          "number_of_sentence",
                                          "average_sentence_length_by_character",
                                          "average_sentence_length_by_word",
                                          "average_word_length"
                                          ])
    table_general.to_csv(output_path_general, header=True, index=True)
    table_number_of_alphabets_az = pd.DataFrame(file_result_az_punc, index=files, columns=ordered_features_az_punc)
    table_number_of_alphabets_az.to_csv(output_path_letters_punc, header=True, index=True)


def generate_statistic(file):
    """
   генерация общей статистики для отдельного файла

   Parameters:

   file: файл для обработки
   """
    global count, complete

    text = get_text_file(file)
    splited_text = text.split("\n")

    # подготовка текста
    feature_dict = get_feature_dict()
    blob = TextBlob(text)
    sentences = blob.sentences
    words = blob.words
    number_of_words = len(words)

    # определение количества символов (буквы, цифры, пробелы, знаки пунктуации, БЕЗ переноса строки!) и отдельно количества букв
    number_of_characters = 0
    number_of_alphabets = 0
    for elem in splited_text:
        for character in elem:
            number_of_characters += 1
            if character.isalpha():
                number_of_alphabets += 1
    feature_dict["number_of_characters"] = number_of_characters
    feature_dict["number_of_alphabets"] = number_of_alphabets

    # определение кол-ва предложений в тексте
    number_of_sentence = len(blob.sentences)
    feature_dict["number_of_sentence"] = number_of_sentence

    # определение кол-ва слов в тексте
    feature_dict["number_of_words"] = number_of_words

    # определение средней длины предложения (по символьно)
    average_sentence_length_by_character = sum((map(lambda sentence: len(sentence), sentences))) / number_of_sentence
    feature_dict["average_sentence_length_by_character"] = average_sentence_length_by_character

    # определение средней длины предложения (по словам)
    general_count = 0
    for sentence in sentences:
        sentence_blob = TextBlob(str(sentence))
        general_count += len(sentence_blob.words)
    average_sentence_length_by_word = general_count / len(sentences)
    feature_dict["average_sentence_length_by_word"] = average_sentence_length_by_word

    # определение средней длины слов
    average_word_length = sum((map(lambda word: len(word), words))) / number_of_words
    feature_dict["average_word_length"] = average_word_length

    complete += 1
    print(complete, ' / ', count)

    return feature_dict


def generate_statistic_az_punc(file):
    """
   генерация статистики по буквам и знаком пунктуации для отдельного файла

   Parameters:

   file: файл для обработки
   """
    text = get_text_file(file)
    feature_dict_az_punc = number_of_alphabets_az_punc(text.lower())
    res = []
    for elem in ordered_features_az_punc:
        res.append(feature_dict_az_punc[elem])

    return res


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


def number_of_alphabets_az_punc(text):
    """
    Функция заполняет словарь feature_dict_az_punc
    :param text: строка, содержащая текст из файла
    :return: заполненный словарь feature_dict_az_punc
    """
    feature_dict_az_punc = get_feature_dict_az_punc()
    punctuations = '.,!@"#№;$%^:&?*()_–-—' + "'"
    for char in text:
        try:
            if char.isalpha():
                feature_dict_az_punc[char] += 1
            elif char in punctuations:
                feature_dict_az_punc[char] += 1
        except Exception as e:
            print("Unsupported symbol " + char + " code " + str(ord(char)))
            print(traceback.format_exc())

    return feature_dict_az_punc

def get_feature_dict():
    """
   Возвращаем стандартный словарь с фичами, где ключ - название фичи, значение - их количество

   """
    return {
        "number_of_characters": 0,
        "number_of_alphabets": 0,
        "number_of_alphabets_az": 0,
        "number_of_punctuation": 0,
        "number_of_words": 0,
        "number_og_sentence": 0,
        "average_word_length": 0,
        "average_sentence_length_by_character": 0,
        "average_sentence_length_by_word": 0
    }


def get_feature_dict_az_punc():
    """
   Возвращаем стандартный словарь с буквами и знаками пунктуации, где ключ - буква или знак, значение - их количество

   """
    return {
        # "a": 0,
        # "b": 0,
        # "c": 0,
        # "d": 0,
        # "e": 0,
        # "f": 0,
        # "g": 0,
        # "h": 0,
        # "i": 0,
        # "j": 0,
        # "k": 0,
        # "l": 0,
        # "m": 0,
        # "n": 0,
        # "o": 0,
        # "p": 0,
        # "q": 0,
        # "r": 0,
        # "s": 0,
        # "t": 0,
        # "u": 0,
        # "v": 0,
        # "w": 0,
        # "x": 0,
        # "y": 0,
        # "z": 0,
        "а": 0,
        "б": 0,
        "в": 0,
        "г": 0,
        "д": 0,
        "е": 0,
        "ё": 0,
        "ж": 0,
        "з": 0,
        "и": 0,
        "й": 0,
        "к": 0,
        "л": 0,
        "м": 0,
        "н": 0,
        "о": 0,
        "п": 0,
        "р": 0,
        "с": 0,
        "т": 0,
        "у": 0,
        "ф": 0,
        "х": 0,
        "ц": 0,
        "ч": 0,
        "ш": 0,
        "щ": 0,
        "ъ": 0,
        "ы": 0,
        "ь": 0,
        "э": 0,
        "ю": 0,
        "я": 0,
        # "ç": 0,
        # "à": 0,
        # "â": 0,
        # "é": 0,
        # "è": 0,
        # "ê": 0,
        # "ë": 0,
        # 'î': 0,
        # "ï": 0,
        # "ô": 0,
        # "ù": 0,
        # "û": 0,
        # "ü": 0,
        # "ÿ": 0,
        ".": 0,
        ",": 0,
        "!": 0,
        "@": 0,
        "'": 0,
        '"': 0,
        "#": 0,
        "№": 0,
        ";": 0,
        "$": 0,
        "%": 0,
        "^": 0,
        ":": 0,
        "&": 0,
        "?": 0,
        "*": 0,
        ")": 0,
        "(": 0,
        "_": 0,
        "–": 0,
        "-": 0,
        "—": 0
    }

if __name__ == "__main__":
    FEATURES_DIR, OUTPUT = get_arguments(HELP_TEXT)
    texts = []
    for filename in os.listdir(FEATURES_DIR):
        if filename.endswith('prd'):
            texts.append(os.path.join(FEATURES_DIR, filename))
    generate_statistics(texts, OUTPUT)
