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

""" This module describes epizeuxis finder """
from functools import partial

from models.feature import Feature
from models.chapter import Chapter
from models.sentence import Sentence


def __find_epizeuxis_inside_sentence(sentence: Sentence, start_count: int, stop_word_check) -> list:
    """Finds epizeuxis in the given sentence

    :param sentence: sentence to find epizeuxis in
    :param start_count: index of first word in sentence
    :param stop_word_check: function checking if word is stop word
    :return: epizeuxis into given sentence (as list of Features)"""
    res = []
    i = 0
    sentence = [word.lower() for word in sentence.words_list]
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


def __find_epizeuxis_between_sentences(chapter: Chapter, start_count: int, stop_word_check) -> list:
    """Finds epizeuxis between sentences in the given chapter

    :param chapter: chapter to find epizeuxis in
    :param start_count: index of first word in chapter
    :param stop_word_check: function checking if word is stop word
    :return: epizeuxis in given chapter (as list of Features)"""
    res = []
    current_feature = None
    chapter = [[word.lower() for word in sentence.words_list] for sentence in chapter.sentences]
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


def find(document) -> list:
    """
    Finds epizeuxis from the document

    :param document: document to find epizeuxis in
    :return: list with epizeuxis (Feature objects)
    """
    res = []
    stop_word_check = partial(document.is_stop_word, 'epizeuxis')
    word_count = 0
    for chapter in document.chapters:
        res.extend(__find_epizeuxis_between_sentences(chapter, word_count, stop_word_check))
        for sentence in chapter:
            res.extend(__find_epizeuxis_inside_sentence(sentence, word_count, stop_word_check))
            word_count += len(sentence)
    return res
