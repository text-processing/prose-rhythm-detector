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


""" This module describes epizeuxis parser """
from functools import partial

from models.document import Document
from models.feature import Feature
from models.text_parser import TextParser


def __parse_epizeuxis_inside_sentence(sentence: list, start_count: int, stop_word_check) -> list:
    """Parses epizeuxis inside the given sentence

    :param sentence: sentence to parse epizeuxis from (as list of words)
    :param start_count: index of first word in sentence
    :param stop_word_check: function checking if word is stop word
    :return: epizeuxis into given sentence (as list of Features)"""
    res = []
    i = 0
    while i < len(sentence) - 1:
        repeat_length, n_of_repeats = 0, 0
        for length in range(1, len(sentence) // 2 + 1):
            if sentence[i:i + length] == sentence[i + length:i + length * 2] and \
                    True not in [stop_word_check(word) for word in sentence[i:i + length]]:
                repeat_length, n_of_repeats = length, 2
                break
        if repeat_length:
            for repeats in range(3, len(sentence[i + repeat_length * 2:]) // repeat_length):
                if sentence[i:i + repeat_length] != \
                        sentence[i + repeat_length * (repeats - 1):i + repeat_length * repeats]:
                    break
                n_of_repeats += 1
            res.append(Feature("epizeuxis", words=[start_count + i + j for j in range(repeat_length * n_of_repeats)],
                               context=[start_count, start_count + len(sentence) - 1]))
            i += repeat_length * n_of_repeats
        else:
            i += 1
    return res


def __parse_epizeuxis_between_sentences(chapter: list, start_count: int, stop_word_check) -> list:
    """Parses epizeuxis between sentences in the given chapter

    :param chapter: chapter to parse epizeuxis in
    :param start_count: index of first word in chapter
    :param stop_word_check: function checking if word is stop word
    :return: epizeuxis in given chapter (as list of Features)"""
    res = []
    current_feature = None
    for i in range(len(chapter) - 1):
        if chapter[i] == chapter[i + 1] and True not in [stop_word_check(word) for word in chapter[i + 1]]:
            if current_feature:
                current_feature.extend_context(start_count + len(chapter[i + 1]))
                for j in range(len(chapter[i + 1])):
                    current_feature.add_word(start_count + len(chapter[i]) + j)
            else:
                current_feature = Feature("epizeuxis",
                                          words=[start_count + j for j in range(len(chapter[i]) + len(chapter[i + 1]))],
                                          context=[start_count, start_count + len(chapter[i]) + len(chapter[i + 1])])
                res.append(current_feature)
        else:
            current_feature = None
        start_count += len(chapter[i])
    return res


def parse(document: Document) -> list:
    """
    Parses epizeuxis from the document

    :param document: document to parse epizeuxis from
    :return: list with epizeuxis (Feature objects)
    """
    res = []
    stop_word_check = partial(document.is_stop_word, 'epizeuxis')
    word_count = 0
    words_by_sent_by_chapt = [list(map(TextParser.split_sentence_to_words, c))
                              for c in TextParser.split_text_to_sentences(document)]
    words_by_sent_by_chapt = [[[word.lower() for word in sentence] for sentence in chapter]
                              for chapter in words_by_sent_by_chapt]
    for chapter in words_by_sent_by_chapt:
        res.extend(__parse_epizeuxis_between_sentences(chapter, word_count, stop_word_check))
        for sentence in chapter:
            res.extend(__parse_epizeuxis_inside_sentence(sentence, word_count, stop_word_check))
            word_count += len(sentence)
    return res
