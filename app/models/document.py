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


"""
This module describes document
"""
import os
import json

from operator import or_
from functools import reduce

import stanfordnlp
from models.feature import Feature
from models.text_parser import TextParser


class Document:
    """
    Class describes document
    """

    def __init__(self, plain_text, chapter_pointers, chapters, language='ru', version=1, features=None):
        if features is None:
            features = list()
        self.__plain_text = plain_text
        self.__plain_text_tokens = list()
        self.__chapter_pointers = chapter_pointers
        self.__version = version
        self.__language = language
        self.__stop_words = self.__read_stop_words()
        self.__features = features
        self.__chapters = chapters
        self.__full_text = list()
        self.__prepare_text()

    def __tokenize_plain_text(self):
        path_to_stanfordnlp_res = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stanfordnlp_resources')
        nlp = stanfordnlp.Pipeline(models_dir=path_to_stanfordnlp_res, processors='tokenize', lang=self.__language)
        doc = nlp(self.__plain_text)
        for i, sentence in enumerate(doc.sentences):
            self.__plain_text_tokens.extend([token.text for token in sentence.tokens])

    def __read_stop_words(self):
        with open('stop_words.json', 'r', encoding='utf-8') as json_file:
            stop_words = json.load(json_file)
        return stop_words[self.language]

    @property
    def language(self):
        """ returns document language """
        return self.__language

    def plain_text(self):
        """ returns plain text of the document """
        return self.__plain_text

    def full_text(self):
        """ returns array of text items"""
        return self.__full_text

    @language.setter
    def language(self, lang):
        """ Set new language to the document """
        self.__language = lang

    def __prepare_text(self):
        """
        Merges the chapters in whole text
        """
        for chapter in self.__chapters:
            self.__full_text.extend(TextParser.split_chapter_by_words(chapter))

    def words_from_to(self, begin: int, end: int):
        """
        :return: a fragment of the text by params
        """
        return self.__full_text[begin:end+1]

    def word_by_index(self, index: int) -> str:
        """
        :return: word at index
        """
        return self.__full_text[index]

    def token_by_index(self, index: int):
        """
        :return: token at index
        """
        return self.__plain_text_tokens[index]

    def words_by_indexes(self, indexes: list):
        """
        :return: list of words by indexes
        """
        words = list()
        for index in indexes:
            words.append(self.word_by_index(index))
        return words

    def fragment_of_plain_text(self, begin: int, end: int):
        """
        :return: a fragment of the text by params
        """
        return self.__plain_text[begin:end]

    def words(self):
        """
        Iterator for the words
        """
        i = 0
        while i < len(self.__full_text):
            yield self.__full_text[i], i
            i += 1

    def add_feature(self, feature):
        """
        Add a new feature to end of feature list
        """
        if isinstance(feature, list):
            self.__features.extend(feature)
        else:
            self.__features.append(feature)

    def features(self):
        """
        Iterator for the features
        """
        for feature in self.__features:
            yield feature

    def feature_types(self) -> list:
        """
        :return: list with all types of the features in the document
        """
        types = set()
        for feature in self.__features:
            types.add(feature.type())
        return list(types)

    def features_with_type(self, feature_type: str) -> list:
        """
        :return: list of features with the specified type
        """
        features = list()
        for feature in self.__features:
            if feature.type() == feature_type:
                features.append(feature)
        return features

    def chapters(self):
        """
        Iterator for the chapters
        """
        for chapter in self.__chapters:
            yield chapter

    def chapter_names(self):
        """
        :return: List of chapter names
        """
        chapters = [self.__plain_text[i:j] for i, j in zip(self.__chapter_pointers,
                                                           self.__chapter_pointers[1:] + [None])]
        return [i.split('\n', 1)[0] for i in chapters]

    def stop_words(self, feature: str):
        """
        :param feature: feature type to get stop words for
        :return: dict of stop words (stop words types as keys) for specified feature
        """
        if feature in self.__stop_words.keys():
            return self.__stop_words[feature]
        return self.__stop_words['anaphora']

    def is_stop_word(self, feature: str, word: str):
        """
        :param feature: feature to test stop word to
        :param word: word from text
        :return: is word is stop word for feature
        """
        if feature in self.__stop_words.keys():
            stop_words = reduce(or_, [set(i) for i in self.__stop_words[feature].values()])
        else:
            stop_words = reduce(or_, [set(i) for i in self.__stop_words['anaphora'].values()])
        return word in stop_words

    def save_to_file(self, file_name="document.prd"):
        """
        Saves current instance of the document to prd format document

        :param file_name: name of file (default document.prd)
        """
        if not file_name.endswith(".prd"):
            file_name += ".prd"
        features_dict = list()
        for item in self.__features:
            features_dict.append(item.to_hash())

        with open(file_name, "w", encoding='utf8') as file:
            file.write(json.dumps({
                "metadata": dict(version=self.__version, language=self.__language),
                "plain_text": self.__plain_text,
                "chapter_pointers": self.__chapter_pointers,
                "text": self.__chapters,
                "features": features_dict},
                                  indent=4, ensure_ascii=False))

        for item in features_dict:
            text_words = list()
            for word in item['words']:
                text_words.append(self.__full_text[word])
            item['words'] = text_words
            item['context'] = ' '.join(self.words_from_to(item['context'][0], item['context'][1]))

    @staticmethod
    def open_from_file(file_name):
        """
        Opens already existing document from *.json file

        :param file_name: name of the document file
        """
        with open(file_name, "r", encoding='utf8') as file:
            json_doc = json.loads(file.read())
            version = json_doc["metadata"]["version"]
            language = json_doc["metadata"]["language"]
            chapter_pointers = json_doc["chapter_pointers"]
            plain_text = json_doc["plain_text"]
            features = list()
            for aspect in json_doc["features"]:
                features.append(Feature(aspect['type'], aspect['words'], aspect['context']))
            chapters = json_doc["text"]
            return Document(plain_text=plain_text, chapter_pointers=chapter_pointers, chapters=chapters,
                            language=language, version=version, features=features)
