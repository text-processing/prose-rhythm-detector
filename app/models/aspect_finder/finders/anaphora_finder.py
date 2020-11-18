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

""" This module describes anaphora finder """
from functools import partial

from models.feature import Feature
from models.text_parser import TextParser


def __find_candidates_to_anaphora_in_chapter(chapter, total_words, candidates, stop_word_check):
    """ Finds candidates to anaphora in the specified chapter"""
    word_count = 0
    i = 0
    while i < len(chapter.sentences):
        if len(chapter.sentences[i]) > 1:
            candidate = Feature('anaphora')
            candidate.add_word(total_words + word_count)
            candidate.add_context(total_words + word_count, total_words + word_count + len(chapter.sentences[i]) - 1)
            word_count += len(chapter.sentences[i])
            first_anaphora_word = chapter.sentences[i][0].lower()
            i += 1
            if stop_word_check(first_anaphora_word):
                continue
            context_length = 1
            while i < len(chapter.sentences) and chapter.sentences[i][0].lower() == first_anaphora_word:
                candidate.extend_context(total_words + word_count + len(chapter.sentences[i]) - 1)
                candidate.add_word(total_words + word_count)
                word_count += len(chapter.sentences[i])
                i += 1
                context_length += 1
            if context_length > 1:
                if candidate not in candidates:
                    candidates.append(candidate)
        else:
            if len(chapter.sentences[i]) > 0 and chapter.sentences[i][0]:
                word_count += len(chapter.sentences[i])
            i += 1
    return word_count


def __extend_anaphora_candidates(candidate, document, stop_word_check):
    """
        Extend to max length the candidates to anaphora
    """
    anaphora_start_word = list()
    for index in candidate.words():
        anaphora_start_word.append(index)

    anaphora_has_max_length = False
    anaphora_length = 1
    while not anaphora_has_max_length:
        repeats = True
        word = TextParser.strip_str(
            document.word_by_index(candidate.context_begin() + anaphora_length).lower())
        for word_index in anaphora_start_word:
            if document.word_by_index(word_index + anaphora_length).lower() != word \
                    or stop_word_check(word):
                repeats = False
        if repeats:
            for word_index in anaphora_start_word:
                candidate.add_word(word_index + anaphora_length)
            anaphora_length += 1
        else:
            anaphora_has_max_length = True


def find(document) -> list:
    """
        Finds anaphora in the specified document

    :param document: document in that will be parsing anaphora
    :return: list with anaphora (Feature objects)
    """
    total_words = 0
    stop_word_check = partial(document.is_stop_word, 'anaphora')
    candidates = list()
    for chapter in document.chapters:
        total_words += __find_candidates_to_anaphora_in_chapter(chapter, total_words, candidates, stop_word_check)
    for candidate in candidates:
        __extend_anaphora_candidates(candidate, document, stop_word_check)
    return candidates
