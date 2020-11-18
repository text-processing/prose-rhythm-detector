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

""" This module describes epiphora finder """
from functools import partial

from models.feature import Feature
from models.chapter import Chapter


def __test_sentences_for_epiphora(sent_1: list, sent_2: list, stop_word_check) -> bool:
    """
        Test two sentences for epiphora

    :param sent_1: first sentence (as list of words)
    :param sent_2: second sentence (as list of words)
    :return: has epiphora between sentences or not
    """
    if len(sent_1) < 1 or len(sent_2) < 1:
        return False
    if sent_1[-1] == sent_2[-1] and not stop_word_check(sent_2[-1]):
        return True
    return False


def __find_epiphora_inside_chapter(chapter: Chapter, start_count: int, stop_word_check) -> list:
    """
        Parses epiphora from chapter

    :param chapter: chapter to find epiphora from (list of sentences as list of words)
    :param start_count: index of first word in chapter
    :param stop_word_check: function checking if word is stop word
    :return: list with epiphora(Feature objects)
    """
    res = []
    word_count = start_count
    current_feature = None
    for i in range(len(chapter.sentences) - 1):
        if __test_sentences_for_epiphora(chapter[i], chapter[i + 1], stop_word_check):
            if current_feature is None:
                current_feature = Feature("epiphora", words=[word_count + len(chapter.sentences[i]) - 1,
                                                             word_count + len(chapter.sentences[i]) + len(chapter.sentences[i + 1]) - 1],
                                          context=[word_count, word_count + len(chapter.sentences[i]) + len(chapter.sentences[i + 1]) - 1])
                res.append(current_feature)
            else:
                current_feature.add_word(word_count + len(chapter[i]) + len(chapter[i + 1]) - 1)
                current_feature.extend_context(word_count + len(chapter[i]) + len(chapter[i + 1]) - 1)
        else:
            current_feature = None
        word_count += len(chapter[i])
    return res


def find(document) -> list:
    """
        Finds epiphora from the specified document

    :param document: document to find epiphora in
    :return: list with epiphora (Feature objects)
    """
    res = []
    stop_word_check = partial(document.is_stop_word, 'epiphora')
    word_count = 0
    for chapter in document.chapters:
        res.extend(__find_epiphora_inside_chapter(chapter, word_count, stop_word_check))
        word_count += sum([len(sent) for sent in chapter])
    return res
