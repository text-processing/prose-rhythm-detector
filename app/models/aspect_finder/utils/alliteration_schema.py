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
""" This module describes schemas of consonant sounds for different languages """
import re


def alliteration_schema(language: str) -> dict:
    """
    :param language: is a language for the consonant sounds schema
    :return: schema of vowel sounds for the specified language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    if language == 'ru':
        return russian_alliteration_schema()
    if language == 'en':
        return english_alliteration_schema()
    if language == 'es':
        return spanish_alliteration_schema()
    if language == 'fr':
        return french_alliteration_schema()
    raise Exception("Language %s is not supported" % language)


def alliteration_sounds(language: str) -> set:
    """ :return: all alliteration sounds for the language """
    if language == 'ru':
        return sounds(russian_alliteration_schema())
    if language == 'en':
        return sounds(english_alliteration_schema())
    if language == 'es':
        return sounds(spanish_alliteration_schema())
    if language == 'fr':
        return sounds(french_alliteration_schema())
    raise Exception("Language %s is not supported" % language)


def sounds(schema: dict):
    """ :return: all sounds the schema contains """
    sounds_at_schema = set()
    for letter, sound_schema in schema.items():
        for sound, _patterns in sound_schema.items():
            sounds_at_schema.add(sound)
    return sounds_at_schema


def find_fragment_at_words(fragment, words) -> dict:
    """
    :return: dict with words and indexes of the word fragment in format: { word: [[indexes]] }
    """
    res = dict()
    for word in words:
        res[word] = [list(range(re.search(fragment, word).regs[0][0], re.search(fragment, word).regs[0][1]))]
    return res


def russian_alliteration_schema():
    """
    :return: schema of consonant sounds for Russian language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    return {
        'б': {
            'б’': {
                'exclusions': [],
                'patterns': [
                    'бь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'б': {
                'exclusions': [],
                'patterns': [
                    'б'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'в': {
            'в’': {
                'exclusions': [],
                'patterns': [
                    'вь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'в': {
                'exclusions': [],
                'patterns': [
                    'в'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'г': {
            'х': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'бог': [[2]]
                }
            },
            'г’': {
                'exclusions': [],
                'patterns': [
                    'гь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'г': {
                'exclusions': [],
                'patterns': [
                    'г'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'д': {
            'д’': {
                'exclusions': [],
                'patterns': [
                    'дь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'д': {
                'exclusions': [],
                'patterns': [
                    'д'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'з': {
            'з’': {
                'exclusions': [],
                'patterns': [
                    'зь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'з': {
                'exclusions': [],
                'patterns': [
                    'з'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'к': {
            'к’': {
                'exclusions': [],
                'patterns': [
                    'кь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'к': {
                'exclusions': [],
                'patterns': [
                    'к'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'л': {
            'л’': {
                'exclusions': [],
                'patterns': [
                    'ль'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'л': {
                'exclusions': [],
                'patterns': [
                    'л'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'м': {
            'м’': {
                'exclusions': [],
                'patterns': [
                    'мь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'м': {
                'exclusions': [],
                'patterns': [
                    'м'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'н': {
            'н’': {
                'exclusions': [],
                'patterns': [
                    'нь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'н': {
                'exclusions': [],
                'patterns': [
                    'н'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'п': {
            'п’': {
                'exclusions': [],
                'patterns': [
                    'пь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'п': {
                'exclusions': [],
                'patterns': [
                    'п'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'р': {
            'р’': {
                'exclusions': [],
                'patterns': [
                    'рь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'р': {
                'exclusions': [],
                'patterns': [
                    'р'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'с': {
            'с’': {
                'exclusions': [],
                'patterns': [
                    'сь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'щ’': {
                'exclusions': [],
                'patterns': [
                    'сч'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'с': {
                'exclusions': [],
                'patterns': [
                    'с'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'т': {
            'ц': {
                'exclusions': [],
                'patterns': [
                    'ть?(?=ся)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'т’': {
                'exclusions': [],
                'patterns': [
                    'ть'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'т': {
                'exclusions': [],
                'patterns': [
                    'т'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ф': {
            'ф’': {
                'exclusions': [],
                'patterns': [
                    'фь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ф': {
                'exclusions': [],
                'patterns': [
                    'ф'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ч': {
            'ч’': {
                'exclusions': [],
                'patterns': [
                    'чь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ш': {
                'exclusions': [],
                'patterns': [
                    'ч(?=то)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ч': {
                'exclusions': [],
                'patterns': [
                    'ч'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'х': {
            'х’': {
                'exclusions': [],
                'patterns': [
                    'хь'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'х': {
                'exclusions': [],
                'patterns': [
                    'х'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ж': {
            'ж': {
                'exclusions': [],
                'patterns': [
                    'ж'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ц': {
            'ц': {
                'exclusions': [],
                'patterns': [
                    'ц'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ш': {
            'ш': {
                'exclusions': [],
                'patterns': [
                    'ш'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'щ': {
            'щ’': {
                'exclusions': [],
                'patterns': [
                    'щ'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
    }


def french_alliteration_schema():
    """
    :return: schema of consonant sounds for French language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    consonants = 'bcçdfgjklmnpqrstvxz'
    vowel = 'aâàiïîyèêeéuûüùôo'
    return {
        'b': {
            'b': {
                'exclusions': [],
                'patterns': [
                    'b'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'c’': {
            's': {
                'exclusions': [],
                'patterns': [
                    'c’[eé]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ç': {
            's': {
                'exclusions': [],
                'patterns': [
                    'ç'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'c': {
            's': {
                'exclusions': [],
                'patterns': [
                    'c(?=[eéèiy])',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'k': {
                'exclusions': [
                    'banc',
                    'tronc'
                    'tabac'
                ],
                'patterns': [
                    'ck'
                    'c'
                ],
                'at_whole_word': [
                    '^ch(?=(lor|ol|or|rét|rist|rom|ron|rys))',
                    '^(?<=i)ch(?=or)',
                    '^(?<=i)ch(?=t)',
                    '^(?<=ma)ch(?=iavel)',
                    '^(?<=psy)ch',
                    '^(?<=tra)ch(?=éo)',
                ],
                'space_at_end': [],
                'space_around': [],

                'words': find_fragment_at_words('ch', [
                    'chaos', 'chaotique', 'chaotiques', 'charadriformes', 'chénopode', 'chiasma',
                    'chiasme', 'chitine', 'chiton', 'chlamydia', 'chlamyde', 'chloasma', 'choeur',
                    'cholagogue', 'chrème', 'chréstomathie', 'ichtyoïde', 'ischémie', 'isochore',
                    'isochrone', 'isochronisme', 'ischémique', 'ischiatique', 'ischion', 'loch',
                    'looch', 'mach', 'machaon', 'manichéisme', 'melchior', 'melchite', 'moloch',
                    'opodeldoch', 'spirochète', 'spirochétose', 'strychos', 'trachyte', 'trachéite',
                    'trachome', 'trochile', 'trochilidés', 'trochiter', 'trochlée', 'tylenchus'])

            },
            'ʃ': {
                'exclusions': [],
                'patterns': [
                    'ch',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('ch', ['psyché', 'psychique', 'psychisme'])
            },
        },
        'd': {
            'd': {
                'exclusions': [],
                'patterns': [
                    'd(?!$)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'f': {
            'f': {
                'exclusions': [],
                'patterns': [
                    'f'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'g': {
            'g': {
                'exclusions': [],
                'patterns': [
                    'g(?!$)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɲ': {
                'exclusions': [],
                'patterns': [
                    'gn'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'Ʒ': {
                'exclusions': [],
                'patterns': [
                    'g[eiy]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'j': {
            'Ʒ': {
                'exclusions': [],
                'patterns': [
                    'j'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'k': {
            'k': {
                'exclusions': [],
                'patterns': [
                    'k'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'l': {
            'l': {
                'exclusions': [],
                'patterns': [
                    'l{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'm': {
            'm': {
                'exclusions': [],
                'patterns': [
                    'm(?=[aeiouyéèêâôîû])'
                ],
                'at_whole_word': [
                    'um$'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('m', ['idem', 'chelem', 'schelem', 'tandem', 'stem', 'modem',
                                                      'ibidem', 'rem', 'requiem'])
            },
        },
        'n': {
            'n': {
                'exclusions': [],
                'patterns': [
                    'n(?=[aeiouyéèêâôîû])'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'with_next_word': [
                    "n(?=\s[aeiouyéêâî])",
                ],
                'words': find_fragment_at_words('n', ['rumen', 'cyclamen', 'larsen', 'lumen', 'volumen', 'golden',
                                                      'gluten', 'graben', 'gramen', 'groschen', 'germen'])

            },
        },
        'p': {
            'f': {
                'exclusions': [],
                'patterns': [
                    'ph'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'p': {
                'exclusions': [],
                'patterns': [
                    'p(?!$)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'q': {
            'k': {
                'exclusions': [],
                'patterns': [
                    'q'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'r': {
            'r': {
                'exclusions': [
                    'fier', 'cher', 'mer', 'amer', 'hier', 'fer', 'hiver', 'vers', 'ber', 'blister', 'cancer',
                    'bunker', 'casher', 'boxer', 'canter', 'eider', 'enfer', 'éther', 'gangster', 'jonkheer',
                    'magister', 'master', 'poker', 'springer', 'starter', 'super', 'trochiter', 'ver', 'vomer',
                    'weber', 'baby-boomer', 'bloomer', 'booster', 'boulder', 'broker', 'cluster', 'cracker',
                    'dealer', 'designer', 'dispatcher', 'dogger', 'driver', 'eye-liner', 'liner', 'putter',
                    'soccer', 'stayer', 'stop-over', 'tanker', 'trader', 'turn-over'
                ],
                'patterns': [
                    'r'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        's': {
            's': {
                'exclusions': [],
                'patterns': [
                    's$',
                    's',
                ],
                'at_whole_word': [
                    '(?<=-viru)s'
                    f'(?<![{vowel}])s(?![{vowel}])',
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'contresens': [[6], [6]], 'vasistas': [[4], [7]], 'oasis': [[4]],
                    'pityriasis': [[9]], 'rhésus': [[5]], 'thésaurus': [[8]]
                }
            },
            'z': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    f'(?<=[{vowel}])s(?=[{vowel}])',
                    f'(?<=^[mtscld]e)s',
                    f'(?<=^vou)s',
                    f'(?<=^nou)s',
                ],
                'space_at_end': [],
                'space_around': [],
                'with_next_word': [
                    "(?<=il)s(?=\s[aeioyéèêàâ]$)",
                    "(?<=che)s(?=\sun$)",
                    "(?<=che)s(?=\sune$)",
                ],
                'words': {
                    'dans': [[3]], 'sans': [[0]], 'sous': [[0]]
                }
            },
        },
        't': {
            't': {
                'exclusions': [],
                'patterns': [
                    't(?![s$])'
                ],
                'at_whole_word': [
                    '(?<=es)t',
                ],
                'with_next_word': [
                    "(?<=on)t(?=\s[aeiouyéêâî])",
                ],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('t', ['déficit', 'digit', 'éfrit'])
            },
        },
        'v': {
            'v': {
                'exclusions': [],
                'patterns': [
                    'v'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'x': {
            'g': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    '(?<=^[aeéiou])x',
                    f'(?<=^y)x(?=[{vowel}])'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'k': {
                'exclusions': [],
                'patterns': [
                    '(?<!(^[aeéiouy]))x(?!$)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'z': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'with_next_word': [
                    "(?<=au)x(?=\s[aeioyéèêàâ])",
                ],
                'words': find_fragment_at_words('x', ['dix', 'six', 'deux'])
            },
        },
        'z': {
            'z': {
                'exclusions': [],
                'patterns': [
                    'z(?!$)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
    }


def english_alliteration_schema():
    """
    :return: schema of consonant sounds for English language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    consonants = 'bcdfghjklmnpqrstvwxz'
    vowels = 'aeiouy'
    return {
        'b': {
            'b': {
                'exclusions': [],
                'patterns': [
                    'b{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'c': {
            's': {
                'exclusions': [],
                'patterns': [
                    'ce',
                    'ci',
                    'cy'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ʃ': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'chic': [[0, 1]]
                }
            },
            'tʃ': {
                'exclusions': [
                    'chic'
                ],
                'patterns': [
                    'ch(?!es)',
                    'tur(?=e)',
                    'tch',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'k': {
                'exclusions': [
                    'chic'
                ],
                'patterns': [
                    'ck',
                    'ch(?!es)',
                    'cu',
                    'c',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'd': {
            'd': {
                'exclusions': [],
                'patterns': [
                    'd{1,2}'
                ],
                'at_whole_word': [
                    '(?<=th)d$',
                    '(?<=the)d$',
                    '(?<=(b|d|g|j|s|v|z|t)e)d$',
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            't': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    '(?<=(ch|sh|th)e)d$',
                    '(?<=(c|f|p|s|h)e)d$',
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'dʒ': {
                'exclusions': [],
                'patterns': [
                    'dge'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'p': {
            'f': {
                'exclusions': [],
                'patterns': [
                    'ph'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'p': {
                'exclusions': [],
                'patterns': [
                    'p{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'q': {
            'k': {
                'exclusions': [],
                'patterns': [
                    'q(?=u)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'f': {
            'v': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'with_next_word': [
                    f'f(?=\s{vowels})'
                ],
                'words': {}
            },
            'f': {
                'exclusions': [],
                'patterns': [
                    'f{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'g': {
            'ʒ': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'garage': [[5]]
                }
            },
            'g': {
                'exclusions': [
                    'German',
                    'genre',
                    'suggest',
                    'manager'
                ],
                'patterns': [
                    'g{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'dʒ': {
                'exclusions': [],
                'patterns': [
                    'g{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('g{1,2}', ['german', 'genre', 'suggest', 'manager'])
            },
            'f': {
                'exclusions': [],
                'patterns': [
                    'qh(?!t)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            't': {
                'exclusions': [],
                'patterns': [
                    'qht'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'h': {
            'h': {
                'exclusions': [],
                'patterns': [
                    '(?<!w)h'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('wh', ['who', 'whose', 'whole'])
            },
        },
        'j': {
            'dʒ': {
                'exclusions': [],
                'patterns': [
                    'j'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'k': {
            'ks': {
                'exclusions': [],
                'patterns': [
                    'kx'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'n': {
                'exclusions': [],
                'patterns': [
                    'kn'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'k': {
                'exclusions': [],
                'patterns': [
                    'k(?!n)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'l': {
            'l': {
                'exclusions': [],
                'patterns': [
                    'l{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'm': {
            'm': {
                'exclusions': [],
                'patterns': [
                    'mb'
                    'm{1,2}',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'n': {
            'w': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('o', ['one', 'once'])
            },
            'ŋ': {
                'exclusions': [],
                'patterns': [
                    'n(?=(g|k))',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'n': {
                'exclusions': [],
                'patterns': [
                    'n{1,2}',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'r': {
            'r': {
                'exclusions': [],
                'patterns': [
                    'r{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        's': {
            'z': {
                'exclusions': [
                    'myself', 'yourself', 'herself', 'himself', 'itself'
                ],
                'patterns': [],
                'at_whole_word': [
                    '(?<=(sh|ss|ch)e)s$',
                    f'(?<=[{vowels}])s(?=[{vowels}])',
                    '(?<=(b|d|j|g|v|z))s',
                    '(?<=th)s'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ʃ': {
                'exclusions': [],
                'patterns': [
                    'sh'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('s', ['sugar', 'sure'])
            },
            'ʒ': {
                'exclusions': [],
                'patterns': [
                    's(?=ion)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('s', ['usually'])
            },
            's': {
                'exclusions': [],
                'patterns': [
                    's{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('sc', ['science', 'scenery'])
            },
        },
        't': {
            'ʃ': {
                'exclusions': [],
                'patterns': [
                    f't(?=i[{vowels}])'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'θ': {
                'exclusions': [
                    'this',
                    'smooth',
                    'with',
                    'within',
                    'thine',
                    'thus',
                    'though',
                    'than',
                    'thy',
                    'that',
                    'those',
                ],
                'patterns': [
                    'th(?=i)'
                ],
                'at_whole_word': [
                    'th$',
                    '^th(?!e)',
                ],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('th', ['theatre', 'thumb', 'healthy', 'author', 'birthday',
                                                       'cathedral', 'catherine', 'theatre', 'lithuania'])
            },
            'ð': {
                'exclusions': [
                    'cathedral',
                    'catherine',
                    'theatre',
                    'lithuania'
                ],
                'patterns': [
                    'th(?=e)',
                    'th'
                ],
                'at_whole_word': [
                    '(?<=i)th'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('th', ['this', 'smooth', 'within', 'thine', 'thus',
                                                       'though', 'than', 'thy', 'that', 'those'])
            },
            't': {
                'exclusions': [],
                'patterns': [
                    't{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'y': {
            'j': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('y', ['yellow', 'yacht', 'yell'])
            },
        },
        'z': {
            'z': {
                'exclusions': [],
                'patterns': [
                    'z'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'w': {
            'r': {
                'exclusions': [],
                'patterns': [
                    'wr'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'w': {
                'exclusions': [],
                'patterns': [
                    'w'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'v': {
            'v': {
                'exclusions': [],
                'patterns': [
                    'v'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
    }


def spanish_alliteration_schema():
    """
    :return: schema of consonant sounds for Spanish language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    return {
        'k': {
            'k': {
                'exclusions': [],
                'patterns': [
                    'k'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'c': {
            'k': {
                'exclusions': [],
                'patterns': [
                    'c[aouáóú]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'kθ': {
                'exclusions': [],
                'patterns': [
                    'cc[eiíé]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'č': {
                'exclusions': [],
                'patterns': [
                    'ch'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'Θ': {
                'exclusions': [],
                'patterns': [
                    'c[eiíé]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'q': {
            'k': {
                'exclusions': [],
                'patterns': [
                    'q'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'n': {
            'm': {
                'exclusions': [],
                'patterns': [
                    'n[mbp]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ŋ': {
                'exclusions': [],
                'patterns': [
                    'n[gk]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'n': {
                'exclusions': [],
                'patterns': [
                    'n'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'p': {
            'p': {
                'exclusions': [],
                'patterns': [
                    'p'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'm': {
            'm': {
                'exclusions': [],
                'patterns': [
                    'm'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'r': {
            'rr': {
                'exclusions': [],
                'patterns': [
                    'rr'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'r': {
                'exclusions': [],
                'patterns': [
                    'r'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'l': {
            'ŷ': {
                'exclusions': [],
                'patterns': [
                    'll'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'l': {
                'exclusions': [],
                'patterns': [
                    'l{1,2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        's': {
            's': {
                'exclusions': [],
                'patterns': [
                    's'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        't': {
            't': {
                'exclusions': [],
                'patterns': [
                    't'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'f': {
            'f': {
                'exclusions': [],
                'patterns': [
                    'f'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'b': {
            'b': {
                'exclusions': [],
                'patterns': [
                    'b'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'v': {
            'v': {
                'exclusions': [],
                'patterns': [
                    'v'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'd': {
            'd': {
                'exclusions': [],
                'patterns': [
                    'd'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'z': {
            'Θ': {
                'exclusions': [],
                'patterns': [
                    'z'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'x': {
            'ks': {
                'exclusions': [],
                'patterns': [
                    'x'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'j': {
            'j': {
                'exclusions': [],
                'patterns': [
                    'j'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'g': {
            'j': {
                'exclusions': [],
                'patterns': [
                    'g[eiéí]'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'g': {
                'exclusions': [],
                'patterns': [
                    'g'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'y': {
            'ŷ': {
                'exclusions': [],
                'patterns': [
                    'y'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ñ': {
            'ñ': {
                'exclusions': [],
                'patterns': [
                    'ñ'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
    }
