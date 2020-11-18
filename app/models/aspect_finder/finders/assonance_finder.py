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
""" This module describes assonance finder """
import re

from models.aspect_finder.utils.assonance_schema import assonance_schema
from models.document import Document
from models.feature import Feature
from models.sentence import Sentence


class AssonanceFinder:
    """ This class describes assonance finder """

    def __init__(self, document: Document):
        self.document = document
        self.schema = assonance_schema(document.lang)
        self.candidates = dict()
        self.word_count = 0
        self.letter_index = 0

    def find(self) -> list:
        """
        Finds assonance in the specified document

        :return: list with assonance (Feature objects)
        """
        assonance = list()
        for chapter in self.document.chapters:
            for sentence in chapter.sentences:
                candidates = self.parse_candidates(sentence)
                assonance.extend(self.__candidates_to_assonance(candidates))
        return assonance

    def parse_candidates(self, sentence: Sentence) -> dict:
        """
        :return: a hash with candidates that has structure:
        {sound: {'words': {word_index: []}, 'context': []}}
        """
        context = [self.word_count, self.word_count + len(sentence) - 1]
        self.candidates = dict()
        for word_index, word in enumerate(sentence.words_list):
            self.letter_index = 0
            while self.letter_index < len(word):
                letter = word[self.letter_index]
                if letter in self.schema.keys():
                    if not self.__find_sound_at_word(sentence, word_index, letter, context):
                        self.letter_index += 1
                else:
                    self.letter_index += 1
        self.word_count += len(sentence)
        return self.__filter_candidates(self.candidates)

    def __find_sound_at_word(self, sentence: Sentence, word_index: int, letter: str, context: list):
        for sound in self.schema[letter]:
            self.__init_candidate(sound, context)
            if not self.__word_is_excluded(sentence[word_index], self.schema[letter][sound]):
                for finder in [self.__find_sound_by_words_patterns,
                               self.__find_sound_by_at_whole_word_patterns,
                               self.__find_sound_by_with_next_word_patterns,
                               self.__find_sound_by_common_patterns,
                               self.__find_sound_by_space_at_end_patterns,
                               self.__find_sound_by_space_around_patterns]:
                    result = finder(sentence, word_index, self.schema[letter][sound])
                    if result:
                        self.__add_candidate(self.candidates[sound], word_index + self.word_count, result)
                        self.__increase_letter_index(result)
                        return True
        return False

    def __init_candidate(self, sound: str, context: list):
        """Initialize the specified sound in the +self.candidates+ field if it is not yet initialized"""
        if sound not in self.candidates:
            self.candidates[sound] = {'context': context, 'words': dict()}

    @classmethod
    def __add_candidate(cls, candidates: dict, word_index: int, letter_indexes: list):
        """
        Add a candidate to candidates dict with specified word index and letter indexes of the word

        :param candidates: is a hash with candidates that has structure:
        {'words': {word_index: []}, 'context': []}
        :param word_index: is a word index of the candidate
        :param letter_indexes: is a list of letter indexes of the word
        """
        if word_index not in candidates['words']:
            candidates['words'][word_index] = list()
        if len(letter_indexes) > 1:
            candidates['words'][word_index].extend(letter_indexes)
        else:
            candidates['words'][word_index].extend(letter_indexes)

    def __increase_letter_index(self, letter_indexes: list):
        self.letter_index += len(letter_indexes)

    @classmethod
    def __range_to_array(cls, begin_end_list) -> list:
        """
        Represents the list of two numbers as a list of numbers from the first value of +begin_end_list+ to
        the second value of +begin_end_list+

        :param begin_end_list: is a list with two numbers
        :return: list of numbers
        """
        return list(range(begin_end_list[0], begin_end_list[1]))

    @classmethod
    def __word_is_excluded(cls, word: str, schema: dict) -> bool:
        """
        Checks that the word is in the exclusions list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': []}

        :return: True if the word is in the exclusion list
        """
        return word in schema['exclusions']

    def __find_sound_by_words_patterns(self, sentence: Sentence, word_index: int, schema: dict):
        """
        Checks that the word is in the word list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': {word: []}}
        :return: list of letter indexes of the sound if a sound was found else None
        """
        if sentence[word_index] in schema['words']:
            for letter_range in schema['words'][sentence[word_index]]:
                if self.letter_index in letter_range:
                    return letter_range
            return schema['words'][sentence[word_index]][0]
        return None

    def __find_sound_by_at_whole_word_patterns(self, sentence: Sentence, word_index: int, schema: dict):
        """
        Checks that the word is matched with a pattern in the 'at_whole_word' pattern list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': {word: []}}
        :return: list of letter indexes of the sound if a sound was found else None
        """
        for pattern in schema['at_whole_word']:
            results = re.finditer(pattern, sentence[word_index])
            if results:
                for result in results:
                    letter_range = self.__range_to_array(result.regs[0])
                    if self.letter_index in letter_range:
                        return letter_range
        return None

    def __find_sound_by_common_patterns(self, sentence: Sentence, word_index: int, schema: dict):
        """
        Checks that the word is matched with a pattern in the 'patterns' pattern list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': {word: []}}
        :return: list of letter indexes of the sound if a sound was found else None
        """
        for pattern in schema['patterns']:
            result = re.match(pattern, sentence[word_index][self.letter_index:])
            if result:
                letter_range = list(map(lambda letter: letter + self.letter_index, result.regs[0]))
                return self.__range_to_array(letter_range)
        return None

    def __find_sound_by_space_at_end_patterns(self, sentence: Sentence, word_index: int, schema: dict):
        """
        Checks that the word is matched with a pattern in the 'space_at_end' pattern list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': {word: []}}
        :return: list of letter indexes of the sound if a sound was found else None
        """
        for pattern in schema.get('space_at_end', dict()):
            if word_index + 1 != len(sentence.words_list):
                result = re.search(pattern, sentence[word_index])
                if result:
                    return self.__range_to_array(result.regs[0])
        return None

    def __find_sound_by_space_around_patterns(self, sentence: Sentence, word_index: int, schema: dict):
        """
        Checks that the word is matched with a pattern in the 'space_around' pattern list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': {word: []}}
        :return: list of letter indexes of the sound if a sound was found else None
        """
        for pattern in schema['space_around']:
            if word_index + 1 != len(sentence.words_list) and word_index - 1 >= 0:
                result = re.search(pattern, sentence[word_index])
                if result:
                    return self.__range_to_array(result.regs[0])
        return None

    def __find_sound_by_with_next_word_patterns(self, sentence: Sentence, word_index: int, schema: dict):
        """
        Checks that the word is matched with a pattern in the 'with_next_word' pattern list of the schema

        :param schema: is a hash that has structure: {'exclusions': [], 'patterns': [], 'at_whole_word': [],
            'space_at_end': [], 'space_around': [], 'words': {word: []}, 'with_next_word': []}
        :return: list of letter indexes of the sound if a sound was found else None
        """
        if word_index + 1 != len(sentence.words_list):
            words = sentence[word_index] + "\s" + sentence[word_index + 1]
            for pattern in schema.get('with_next_word', dict()):
                result = re.search(pattern, words)
                if result:
                    return self.__range_to_array(result.regs[0])
        return None

    @classmethod
    def __filter_candidates(cls, candidates: dict) -> dict:
        """
        :param candidates: is a hash with candidates that has structure:
        {sound: {'words': {word_index: []}, 'context': []}}
        :return: candidates in the same structure where length of 'words' value is more than 1
        """
        filtered_candidates = dict()
        for sound in candidates.keys():
            if len(candidates[sound]['words']) > 1:
                filtered_candidates[sound] = candidates[sound]
        return filtered_candidates

    def __candidates_to_assonance(self, candidates: dict) -> list:
        """
        :param candidates: is a hash with candidates that has structure:
        {sound: {'words': {word_index: []}, 'context': []}}
        :return: list of Feature objects created from the candidates
        """
        return self.candidates_to_feature(candidates, 'assonance')

    @classmethod
    def candidates_to_feature(cls, candidates: dict, feature_type: str) -> list:
        """
        :param feature_type: is a type of features
        :param candidates: is a hash with candidates that has structure:
        {sound: {'words': {word_index: []}, 'context': []}}
        :return: list of Feature objects created from the candidates
        """
        features = list()
        for sound in candidates.keys():
            words = list(candidates[sound]['words'].keys())
            feature = Feature(feature_type, words, candidates[sound]['context'],
                              candidates[sound]['words'], sound)
            features.append(feature)
        return features
