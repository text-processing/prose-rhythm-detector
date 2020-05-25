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
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
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

# словари для n-грамм
ngram1_dict = dict()
ngram2_dict = dict()
ngram3_dict = dict()
ngram4_dict = dict()


def generate_statistics(files, output_path_general, output_path_ngram1, output_path_ngram2, output_path_ngram3,
                        output_path_ngram4, output_path_letters_punc, language):
    """
   входная точка в утилиту, которые формирует статискику для всех файлов

   Parameters:

   files: список файлов, подаваемых на вход утилите для дальнейшей обработки
   output_path_general: имя файла, где будет располагаться результат работы утилиты по общим характеристикам
   output_path_ngramN: имена файлов, где будут храниться результаты работы утилиты по конкретным n-граммам (N - кол-во слов в n-граммам)
   language: язык обрабатываемых текстов
   """

    open(output_path_general, 'w').close()
    open(output_path_ngram1, 'w').close()
    open(output_path_ngram2, 'w').close()
    open(output_path_ngram3, 'w').close()
    open(output_path_ngram4, 'w').close()
    open(output_path_letters_punc, 'w').close()

    # Итерируем список файлов и результат статистики пишем в качестве строки в файл

    pool = ThreadPool(len(files))
    results = pool.starmap(generate_statistic, zip(files))
    results_az_punc = pool.starmap(generate_statistic_az_punc, zip(files))
    pool.close()
    pool.join()

    ngram1_dict_sorted = sorted(ngram1_dict.items(), key=lambda kv: kv[1], reverse=True)
    ngram1_list = list()
    for elem in ngram1_dict_sorted[:40]:
        ngram1_list.append(elem[0])
    for elem in ngram1_dict_sorted[:40]:
        ngram1_list.append(elem[1])

    ngram2_dict_sorted = sorted(ngram2_dict.items(), key=lambda kv: kv[1], reverse=True)
    ngram2_list = list()
    for elem in ngram2_dict_sorted[:40]:
        ngram2_list.append(elem[0])
    for elem in ngram2_dict_sorted[:40]:
        ngram2_list.append(elem[1])

    ngram3_dict_sorted = sorted(ngram3_dict.items(), key=lambda kv: kv[1], reverse=True)
    ngram3_list = list()
    for elem in ngram3_dict_sorted[:40]:
        ngram3_list.append(elem[0])
    for elem in ngram3_dict_sorted[:40]:
        ngram3_list.append(elem[1])

    ngram4_dict_sorted = sorted(ngram4_dict.items(), key=lambda kv: kv[1], reverse=True)
    ngram4_list = list()
    for elem in ngram4_dict_sorted[:40]:
        ngram4_list.append(elem[0])
    for elem in ngram4_dict_sorted[:40]:
        ngram4_list.append(elem[1])

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

    table_ngram1 = make_csv_ngram(ngram1_list, files)
    table_ngram1.to_csv(output_path_ngram1, header=True, index=True)

    table_ngram2 = make_csv_ngram(ngram2_list, files)
    table_ngram2.to_csv(output_path_ngram2, header=True, index=True)

    table_ngram3 = make_csv_ngram(ngram3_list, files)
    table_ngram3.to_csv(output_path_ngram3, header=True, index=True)

    table_ngram4 = make_csv_ngram(ngram4_list, files)
    table_ngram4.to_csv(output_path_ngram4, header=True, index=True)

    table_number_of_alphabets_az = make_csv_number_of_alphabets_az(file_result_az_punc, files)
    table_number_of_alphabets_az.to_csv(output_path_letters_punc, header=True, index=True)


def generate_statistic(file):
    """
   генерация общей статистики для отдельного файла

   Parameters:

   file: файл для обработки
   """
    global ngram1_dict, ngram2_dict, ngram3_dict, ngram4_dict

    print("Start preparing")
    text = get_text_file(file)
    splited_text = text.split("\n")

    # создание отдельного объекта TextBlob без знаков пунктуации для подсчёта n-грамм
    STOP_PUNC = '– - — ! @ # $ % ^ & * ( ) + = _ ? № ; : "'.split()
    ngram1_text = ""
    for word in text:
        if word in STOP_PUNC:
            continue
        else:
            ngram1_text += word
    blob_ngram = TextBlob(ngram1_text)

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

    # определение n-грамм для конкретного текста
    get_ngram(blob_ngram, 1, ngram1_dict)
    get_ngram(blob_ngram, 2, ngram2_dict)
    get_ngram(blob_ngram, 3, ngram3_dict)
    get_ngram(blob_ngram, 4, ngram4_dict)

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
    print("Start preparing")
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


def make_csv_number_of_alphabets_az(file_result_az_punc, files):
    """
    Функция, которая составляет csv-таблицу для букв и символов пунктуации
    :param file_result_az_punc: список с результатами
    :param files: файл для обработки
    :return: csv-таблицу
    """
    table = pd.DataFrame(file_result_az_punc, index=files,
                         columns=ordered_features_az_punc)
    return (table)


def get_ngram(blob, length, ngram_dict):
    """
    Функция для получение n-грамм заданной длинны 1 <= n <= 4 с учётом стоп-слов
    :param blob: объект textblob, содержащий в себе текст из обрабанываемого файла
    :param length: длинна n-граммы
    :param ngram_dict: глобальный словарь для записи n-грамм
    :return:
    """
    STOP_WORDS = 'I it my your his her its our their a the by for in on to в к с на о об обо во ко со по под за до над ' \
                 'от ото пред при у вне me us you him them this that - ! @ # $ % ^ & * ( ) + = _ — ? № ; : " '.split()
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


def make_csv_ngram(ngram_list, files):
    """
    Функция, которая составляет csv-таблицу для n-грамм, в зависимости от количество слов в ней
    :param ngram_list: список n-грамм из глобального словаря
    :param files: файлы для обработки
    :return: csv-таблицу
    """
    ngram_result = []
    results_list = []
    for ngram in ngram_list[40:]:
        try:
            results_list.append(str(ngram))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
    ngram_result.append(results_list)
    table = pd.DataFrame(ngram_result, index=files,
                         columns=[ngram_list[0],
                                  ngram_list[1],
                                  ngram_list[2],
                                  ngram_list[3],
                                  ngram_list[4],
                                  ngram_list[5],
                                  ngram_list[6],
                                  ngram_list[7],
                                  ngram_list[8],
                                  ngram_list[9],
                                  ngram_list[10],
                                  ngram_list[11],
                                  ngram_list[12],
                                  ngram_list[13],
                                  ngram_list[14],
                                  ngram_list[15],
                                  ngram_list[16],
                                  ngram_list[17],
                                  ngram_list[18],
                                  ngram_list[19],
                                  ngram_list[20],
                                  ngram_list[21],
                                  ngram_list[22],
                                  ngram_list[23],
                                  ngram_list[24],
                                  ngram_list[25],
                                  ngram_list[26],
                                  ngram_list[27],
                                  ngram_list[28],
                                  ngram_list[29],
                                  ngram_list[30],
                                  ngram_list[31],
                                  ngram_list[32],
                                  ngram_list[33],
                                  ngram_list[34],
                                  ngram_list[35],
                                  ngram_list[36],
                                  ngram_list[37],
                                  ngram_list[38],
                                  ngram_list[39]
                                  ])
    return (table)


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
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
        "e": 0,
        "f": 0,
        "g": 0,
        "h": 0,
        "i": 0,
        "j": 0,
        "k": 0,
        "l": 0,
        "m": 0,
        "n": 0,
        "o": 0,
        "p": 0,
        "q": 0,
        "r": 0,
        "s": 0,
        "t": 0,
        "u": 0,
        "v": 0,
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
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
    generate_statistics(texts, OUTPUT, 'en')
