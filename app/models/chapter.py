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

from models.sentence import Sentence, SentenceStructures


class Chapter:
    """
    Program representation of chapter.
    """

    def __init__(self, model, title, lang):
        self.model = model
        self.sentences = list(filter(lambda x: len(x.words_list) > 0,
                                     (Sentence(sentence) for sentence in model.sentences)))
        self.title = title
        self.lang = lang

    @property
    def words_list(self):
        return [sentence.words_list for sentence in self.sentences]

    def sentence_successors(self, sentence_index):
        if self[sentence_index].structure_type != SentenceStructures.SIMPLE:
            tail = self[sentence_index].tail
        else:
            tail = None
        next = self[sentence_index + 1] if sentence_index + 1 < len(self.sentences) else None
        return [successor for successor in [tail, next] if successor is not None]

    def __getitem__(self, key):
        return self.sentences[key]

    def __len__(self):
        return sum(len(sentence) for sentence in self.sentences)

    def __repr__(self):
        return f"Chapter {self.title}, length: {len(self)}"

    def __str__(self):
        return '[' + '\n'.join(str(sentence) for sentence in self.sentences) + ']'
