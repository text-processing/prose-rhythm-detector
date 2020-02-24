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


""" This module describes conjunctions, pair conjunctions and conjunctive adverbs """


def conjunctions(language: str) -> set:
    """
    :param language: language to get conunctions for
    :return: set of all conjunctions in language
    """
    try:
        return {'ru': {"а", "будто", "где", "едва", "да", "дабы", "ежели", "если", "зато", "зачем", "и", "ибо", "или",
                       "кабы", "как", "каков", "какой", "когда", "коли", "который", "кто", "куда", "лишь", "насколько",
                       "нежели", "но", "однако", "откуда", "отчего", "пока", "поскольку", "потому", "почему", "поэтому",
                       "пускай", "пусть", "раз", "сколько", "словно", "также", "тоже", "только", "точно", "хотя", "чей",
                       "чем", "что", "чтобы"},
                'en': {"and", "as", "for", "or", "yet", "but", "till", "as", "if", "after", "until", "because", "and",
                       "or", "nor", "so", "before", "since", "that", "unless", "whether", "while", "where", "when",
                       "why", "what", "how", "whenever", "although", "though", "once", "than", "whereas", "thus",
                       "in case", "on condition", "who", "which", "whose"}
                }[language]
    except KeyError:
        raise Exception("Language %s is not supported" % language)


def pair_conjunctions(language: str) -> set:
    """
    :param language: language to get pair conunctions for
    :return: set of all pair conjunctions (as tuples) in language
    """
    try:
        return {'ru': {},
                'en': {("both", "and"), ("either", "or"), ("not only", "but"), ("not only", "but also"),
                       ("rather", "or"), ("just as", "so"), ("neither", "nor"), ("whether", "or"), ("if", "then")}
                }[language]
    except KeyError:
        raise Exception("Language %s is not supported" % language)


def conjunctive_adverbs(language: str) -> set:
    """
    :param language: language to get conjuctive adverbs for
    :return: set of all conjuctive adverbs in language
    """
    try:
        return {'ru': {("благодаря", "тому", "что"), ("в", "связи", "с"), ("в", "связи", "с", "тем", "что"),
                       ("в", "то", "время", "как"), ("ввиду", "того", "что"), ("вследствие", "того", "что"),
                       ("для", "того", "чтобы"), ("до", "тех", "пор", "пока"), ("если", "бы"), ("затем", "чтобы"),
                       ("из-за", "того", "что"), ("как", "будто"), ("как", "если", "бы"), ("как", "только"),
                       ("лишь", "только"), ("не", "смотря", "на", "то", "что"), ("оттого", "что"),
                       ("перед", "тем", "как"), ("по", "мере", "того", "как"), ("подобно", "тому", "как"),
                       ("пока", "не"), ("после", "того", "как"), ("потому", "что"), ("прежде", "чем"),
                       ("с", "тем", "чтобы"), ("с", "тех", "пор", "как"), ("так", "как"), ("так", "что")},
                'en': {("after", "all"), ("also",), ("as", "a", "result"), ("besides",), ("consequently",),
                       ("for", "example"), ("however",), ("in", "addition"), ("in", "fact"), ("in", "other", "words"),
                       ("meanwhile",), ("moreover",), ("on", "the", "other", "hand"), ("therefore",), ("thus",),
                       ("then",)}
                }[language]
    except KeyError:
        raise Exception("Language %s is not supported" % language)
