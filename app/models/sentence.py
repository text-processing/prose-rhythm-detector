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

from enum import Enum, auto


class SentenceStructures(Enum):
    """
    Sentence structure types
    information source: https://en.wikipedia.org/wiki/Sentence_(linguistics)
    """
    SIMPLE = auto()
    COMPOUND = auto()
    COMPLEX = auto()


class Sentence:
    """
    Program representation of sentence
    """

    def __init__(self, model):
        self.model = model
        self.structure_type = self.structure_type(model)  # TODO write test for me

    @property
    def text(self):
        return self.model.text

    @staticmethod
    def structure_type(model):
        # TODO Разработать систему проверки
        for word in model.words:
            if word.deprel == 'ccomp':
                return SentenceStructures.COMPLEX
        return SentenceStructures.SIMPLE

    @property
    def tail(self):
        return None  # TODO implement me

    @property
    def ending_punct(self):
        ending = []
        for word in self.model.words[::-1]:
            if word.upos != "PUNCT":
                break
            ending.insert(0, word.text)
        return ''.join(ending)

    @property
    def words_list(self):
        """ List of words in sentence (excluding punctuation and symbols) """
        return [word.text.lower() for word in self.model.words if word.pos not in {"PUNCT", "SYM"}]

    def __getitem__(self, key):
        return self.words_list[key]

    def __len__(self):
        """
        :return: number of words in sentence
        """
        return len(self.words_list)

    def __str__(self):
        return '["' + '", "'.join(word.text for word in self.model.words) + '"]'

    def __repr__(self):
        return f"Sentence, length = {len(self)}"
