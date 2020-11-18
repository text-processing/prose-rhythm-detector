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

""" This module describes alliteration finder """
from models.aspect_finder.finders.assonance_finder import AssonanceFinder
from models.aspect_finder.utils.alliteration_schema import alliteration_schema
from models.document import Document


class AlliterationFinder(AssonanceFinder):
    """ This class describes alliteration finder """

    def __init__(self, document: Document):
        super().__init__(document)
        self.schema = alliteration_schema(document.lang)

    def find(self) -> list:
        """
        Finds alliteration in the specified document

        :return: list with alliteration (Feature objects)
        """
        alliterations = list()
        for chapter in self.document.chapters:
            for sentence in chapter.sentences:
                candidates = self.parse_candidates(sentence)
                alliterations.extend(self.__candidates_to_alliteration(candidates))
        return alliterations

    def __candidates_to_alliteration(self, candidates: dict) -> list:
        """
        :param candidates: is a hash with candidates that has structure:
        {sound: {'words': {word_index: []}, 'context': []}}
        :return: list of Feature objects created from the candidates
        """
        return self.candidates_to_feature(candidates, 'alliteration')
