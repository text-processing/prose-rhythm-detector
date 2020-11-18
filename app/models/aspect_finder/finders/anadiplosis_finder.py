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

""" This module describes anadiplosis parser """
from functools import partial

from models.feature import Feature


def __test_sentences_for_anadiplosis(first_sent: list, second_sent: list, stop_word_check) -> dict:
    """
    Test two sentences (as list of words) first and second for anadiplosis
    :param first:
    :param second:
    :param stop_word_check: function checking if word is stop word
    :return: dict{words:repeating words, metric: importance metric}
    """
    # Not implemented: processing prepositions such as 'a' and 'the'
    # checking for andiplosis for number of words from len of (shorter sentence - 1) to 1
    # (if sentence fully repeating, it is lexic repeat)
    first = [w.lower() for w in first_sent]
    second = [w.lower() for w in second_sent]
    for size in range(min(map(len, (first, second))) - 1, 0, -1):
        if first[-size:] == second[:size] and True not in [stop_word_check(word) for word in first[-size:]]:
            return {'words': first[-size:], 'metric': size}
    return {'words': [], 'metric': 0}


def __find_anadiplosis_inside_chapter(chapter: list, start_count: int, stop_word_check) -> list:
    """
    :param chapter: chapter as list of sentences (as list of words)
    :param start_count: index of first word in chapter
    :return: list of Features
    """
    threshold = 1  # minimal metric
    res = []
    word_count = start_count
    for i in range(len(chapter) - 1):
        candidate = __test_sentences_for_anadiplosis(chapter[i], chapter[i + 1], stop_word_check)
        if candidate['metric'] >= threshold:
            res.append(Feature(feature_type="anadiplosis",
                               words=[n + word_count + len(chapter[i]) for n in range(-len(candidate['words']),
                                                                                      len(candidate['words']))],
                               context=[word_count, word_count + len(chapter[i]) + len(chapter[i + 1]) - 1]))
        word_count += len(chapter[i])
    return res


def find(document) -> list:
    """
        Finds anadiplosis in the specified document

    :param document: document in that will be parsing anadiplosis
    :return: list with anadiplosis (Feature objects)
    """
    res = []
    stop_word_check = partial(document.is_stop_word, 'anadiplosis')
    word_count = 0
    for chapter in document.words_list:
        res.extend(__find_anadiplosis_inside_chapter(chapter, word_count, stop_word_check))
        word_count += sum(len(sent) for sent in chapter)
    return res
