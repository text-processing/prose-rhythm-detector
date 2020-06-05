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


""" This module describes diacope parser """

from itertools import product
from functools import reduce
from operator import add

from models.aspect_parser.utils.conjunctions import conjunctions
from models.document import Document
from models.feature import Feature
from models.text_parser import TextParser
from models.aspect_parser.utils.merge_features import merge_features


def __diacope_words(word_positions: list) -> list:
    """
    Tests word positions in sentence for diacope (to disregard, for example, reduplication)

    :param word_positions: list with word positions in sentence
    :return: list with positions of words forming diacope
    """
    return [position for position in word_positions if position - 1 not in word_positions]


def __merge_diacope_in_nearby_words_inside_sentence(diacope: list) -> list:
    """
    Merges diacope in nearby words

    :param diacope: diacope to merge if they are in nearby words (list of Features)
    :returns: list with merged and unchanged diacope
    """
    min_power_to_merge = 2
    diacope.sort(key=lambda x: x.word_at_index(0))
    i = 0
    while i < len(diacope) - 1:
        power = 0
        for word_a, word_b in product(diacope[i].words(), diacope[i + 1].words()):
            if word_b == word_a + 1:
                power += 1
        if power >= min_power_to_merge and power == diacope[i + 1].words_length():
            diacope[i] = merge_features(diacope[i], diacope[i + 1])
            del diacope[i + 1]
        else:
            i += 1
    return diacope


def __parse_diacope_inside_sentence(sent: list, start_count: int, excluded_words: set) -> list:
    """
    Parses diacope from the specified sentence

    :param sent: sentence to parse diacope from (as list of words)
    :param start_count: index of first word in sentence
    :param excluded_words: set of words which can't be part of diacope
    :return: list with diacope in sentence
    """
    min_diacope_power = 2
    res = []
    for word in set(sent) - excluded_words:
        word_positions = [i for i, w in enumerate(sent) if w == word]
        if len(word_positions) >= min_diacope_power:
            diacope_positions = __diacope_words(word_positions)
            if len(diacope_positions) >= min_diacope_power:
                res.append(Feature("diacope", [start_count + pos for pos in diacope_positions],
                                   [start_count, start_count + len(sent) - 1]))
    res = __merge_diacope_in_nearby_words_inside_sentence(res)
    return res


def __parse_diacope_inside_chapter(chapter: list, start_count: int, excluded_words: set) -> list:
    """
    Parses diacope from the specified chapter

    :param chapter: chapter to parse diacope from (as list of sentences)
    :param start_count: index of first word in chapter
    :param excluded_words: set of words which can't be part of diacope
    :return: list with diacope in chapter
    """

    res = []
    word_count = start_count
    for sent in chapter:
        sentence = [word.lower() for word in sent]
        res.extend(__parse_diacope_inside_sentence(sentence, word_count, excluded_words))
        word_count += len(sentence)
        # объединить диакопы предложений?
    return res


def parse(document: Document) -> list:
    """
    Parses diacope from the specified document

    :param document: document to parse diacope from
    :return: list with diacope (Feature objects)
    """
    stop_words = set(reduce(add, document.stop_words('diacope').values()))
    excluded_words = set(conjunctions(document.language)) | stop_words
    res = []
    words_by_sent_by_chapter = [list(map(TextParser.split_sentence_to_words, s))
                                for s in TextParser.split_text_to_sentences(document)]
    word_count = 0
    for chapter in words_by_sent_by_chapter:
        res.extend(__parse_diacope_inside_chapter(chapter, word_count, excluded_words))
        word_count += sum([len(sent) for sent in chapter])
    return res
