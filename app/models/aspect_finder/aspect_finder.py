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
""" This module describes aspect finder """
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from PySide2.QtCore import QObject, Signal

from models.aspect_finder.finders import anaphora_finder, epiphora_finder, symploce_finder, \
    anadiplosis_finder, polysyndeton_finder, epizeuxis_finder, diacope_finder, epanalepsis_finder, chiasmus_finder, \
    aposiopesis_finder, exclamatory_interrogative_sequences_finder
from models.aspect_finder.finders.alliteration_finder import AlliterationFinder
from models.aspect_finder.finders.assonance_finder import AssonanceFinder


class AspectFinder(QObject):
    """ Class describes Aspect Finder """
    update_progress = Signal(int, int)

    def __init__(self, document, progress_bar=None):
        super().__init__()
        self.document = document
        self.progress = 0

    def find_anaphora(self) -> list:
        """
        Finds anaphora in the document

        :return: list with anaphora (list of Feature objects)
        """
        return anaphora_finder.find(self.document)

    def find_anadiplosis(self) -> list:
        """
        Finds anadiplosis in the document

        :return: list with anadiplosis (list of Feature objects)
        """
        return anadiplosis_finder.find(self.document)

    def find_polysyndeton(self) -> list:
        """
        Finds polysyndeton in the document

        :return: list with polysyndeton (list of Feature objects)
        """
        return polysyndeton_finder.find(self.document)

    def find_epiphora(self) -> list:
        """
        Finds epiphora in the document

        :return: list with epiphora (list of Feature objects)
        """
        return epiphora_finder.find(self.document)

    @staticmethod
    def find_symploce(anaphoras: list, epistrophas: list) -> list:
        """
        Finds symploce in the document

        :param anaphoras: list with anaphora found in the document
        :param epistrophas: list with epistrophas found in the document
        :return: list with symploce (list of Feature objects)
        """
        return symploce_finder.find(anaphoras, epistrophas)

    def find_recurring_sentence_parts_features(self) -> list:
        """
        Finds recurring sentence parts features (anaphora, epiphora and symploce) in the
        document

        :return: list with anaphora, epiphora and symploce
        """
        anaphoras = self.find_anaphora()
        epiphoras = self.find_epiphora()
        symploces = self.find_symploce(anaphoras, epiphoras)
        return anaphoras + epiphoras + symploces

    def find_epizeuxis(self) -> list:
        """
        Finds epizeuxis in the document

        :return: list with epizeuxis (Feature objects)
        """
        return epizeuxis_finder.find(self.document)

    def find_diacope(self) -> list:
        """
        Finds diacope in the document

        :return: list with diacope (Feature objects)
        """
        return diacope_finder.find(self.document)

    def find_epanalepsis(self) -> list:
        """
        Finds epanalepsis from the document

        :return: list with epanalepsis (Feature objects)
        """
        return epanalepsis_finder.find(self.document)

    def find_chiasmus(self) -> list:
        """
        Finds chiasmus in the document

        :return: list with chiasmus (Feature objects)
        """
        return chiasmus_finder.find(self.document)

    def find_assonance(self) -> list:
        """
        Finds assonance from the document

        :return: list with assonance (Feature objects)
        """
        finder = AssonanceFinder(self.document)
        return finder.find()

    def find_alliteration(self) -> list:
        """
        Finds alliteration from the document

        :return: list with alliteration (Feature objects)
        """
        finder = AlliterationFinder(self.document)
        return finder.find()

    def find_repeating_ending_sentences(self) -> list:
        """
        Finds sentence with repeating endings (for example, ellipses)

        :return: list with Features
        """
        res = aposiopesis_finder.find(self.document) + \
              exclamatory_interrogative_sequences_finder.find(self.document)
        return res

    def find(self) -> list:
        result = []
        futures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures.extend([
                executor.submit(self.find_recurring_sentence_parts_features),
                executor.submit(self.find_anadiplosis),
                executor.submit(self.find_polysyndeton),
                executor.submit(self.find_diacope),
                executor.submit(self.find_epizeuxis),
                executor.submit(self.find_epanalepsis),
                executor.submit(self.find_chiasmus),
                executor.submit(self.find_assonance),
                executor.submit(self.find_alliteration),
                executor.submit(self.find_repeating_ending_sentences)
            ])
            self.update_progress.emit(self.progress, len(futures))
            for future in as_completed(futures):
                result += future.result()
                self.progress += 1
                self.update_progress.emit(self.progress, len(futures))
        return result
