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

""" This module describes epanalepsis finder """
from functools import partial

from models.feature import Feature


def __find_epanalepsis_inside_sentence(sentence: list, start_index: int, stop_word_check) -> list:
    """
    Finds epanalepsis from the specified sentence

    :param sentence: sentence to find epanalepsis in
    :param start_index: index of first word in sentence
    :param stop_word_check: function checking if word is stop word
    :return: epanalepsis inside the sentence (as list of Features)
    """
    # Оставлен задел под сложное предложение (в таком случае предложение может содержать несколько эпаналепсисов)
    res = []
    repeat_length = 0
    for length in range(1, len(sentence) // 2 + 1):
        if sentence[:length] == sentence[-length:] and \
                True not in [stop_word_check(word) for word in sentence[:length]]:
            repeat_length = length
    if repeat_length:
        res.append(Feature("epanalepsis",
                           words=[start_index + i for i in range(repeat_length)] +
                                  [start_index + len(sentence) - i for i in range(repeat_length, 0, -1)],
                           context=[start_index, start_index + len(sentence) - 1]))
    return res


def find(document) -> list:
    """Finds epanalepsis in the specified document

    :param document: document to find epanalepsis in
    :return: epanalepsis in the document (as list of Features)"""
    res = []
    stop_word_check = partial(document.is_stop_word, 'epanalepsis')
    word_count = 0
    words_by_sent_by_chapt = [[[word.lower() for word in sentence.words_list] for sentence in chapter]
                              for chapter in document.chapters]
    for chapter in words_by_sent_by_chapt:
        for sentence in chapter:
            res.extend(__find_epanalepsis_inside_sentence(sentence, word_count, stop_word_check))
            word_count += len(sentence)
    return res
