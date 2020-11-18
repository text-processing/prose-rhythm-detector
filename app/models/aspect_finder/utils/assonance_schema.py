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
""" This module describes schemas of vowel sounds for different languages """
from models.aspect_finder.utils.alliteration_schema import find_fragment_at_words, sounds


def assonance_schema(language: str) -> dict:
    """
    :param language: is a language for the vowel sounds schema
    :return: schema of vowel sounds for the specified language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    if language == 'ru':
        return russian_assonance_schema()
    if language == 'en':
        return english_assonance_schema()
    if language == 'es':
        return spanish_assonance_schema()
    if language == 'fr':
        return french_assonance_schema()
    raise Exception("Language %s is not supported" % language)


def assonance_sounds(language: str) -> set:
    """ :return: all assonance sounds for the language """
    if language == 'ru':
        return sounds(russian_assonance_schema())
    if language == 'en':
        return sounds(english_assonance_schema())
    if language == 'es':
        return sounds(spanish_assonance_schema())
    if language == 'fr':
        return sounds(french_assonance_schema())
    raise Exception("Language %s is not supported" % language)


def russian_assonance_schema():
    """
    :return: schema of vowel sounds for Russian language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    return {
        'а': {
            'а': {
                'exclusions': [],
                'patterns': [
                    'а'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'о': {
            'о': {
                'exclusions': [],
                'patterns': [
                    '(?<!о)о(?!о)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'а': {
                'exclusions': [],
                'patterns': [
                    'о{2}'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'у': {
            'у': {
                'exclusions': [],
                'patterns': [
                    'у'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ы': {
            'ы': {
                'exclusions': [],
                'patterns': [
                    'ы'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'э': {
            'э': {
                'exclusions': [],
                'patterns': [
                    'э'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'и': {
            'и': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    '(?<!(ж|ш|ц))и'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ы': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    '(?<=(ж|ш|ц))и',
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'я': {
            'йа': {
                'exclusions': [],
                'patterns': [
                    'я'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ё': {
            'йо': {
                'exclusions': [
                    "принёсший",
                    "поблёкший",
                    "привёзший",
                    "плётший",
                    "затёкший"
                ],
                'patterns': [
                    'ё'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'о': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    "принёсший": [[4]],
                    "поблёкший": [[4]],
                    "привёзший": [[4]],
                    "плётший": [[2]],
                    "затёкший": [[3]]
                }
            },
        },
        'ю': {
            'йу': {
                'exclusions': [],
                'patterns': [
                    'ю'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'е': {
            'йэ': {
                'exclusions': [],
                'patterns': [
                    'е'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        }
    }


def french_assonance_schema():
    """
    :return: schema of vowel sounds for French language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    consonants = 'bcçdfgjklmnpqrstvxz'
    return {
        'a': {
            'aj': {
                'exclusions': [],
                'patterns': [
                    'aill'
                ],
                'space_at_end': [],
                'at_whole_word': [
                    'ail$'
                ],
                'space_around': [],
                'words': {}
            },
            'ɔ': {
                'exclusions': [],
                'patterns': [
                    'aur'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'a͂': {
                'exclusions': [],
                'patterns': [
                    'a(?=[nm])',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'o': {
                'exclusions': [],
                'patterns': [
                    'au(?!r)',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɛ͂': {
                'exclusions': [],
                'patterns': [
                    'ain',
                    'aim',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɛ': {
                'exclusions': [],
                'patterns': [
                    'ai',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'a': {
                'exclusions': [],
                'patterns': [
                    "a"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'â': {
            'a': {
                'exclusions': [],
                'patterns': [
                    "â"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'à': {
            'a': {
                'exclusions': [],
                'patterns': [
                    "à"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'é': {
            'e': {
                'exclusions': [],
                'patterns': [
                    "é"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'e': {
            'ɛ': {
                'exclusions': [],
                'patterns': [
                    "e(?=(bb|cc|dd|ff|gg|kk|ll|mm|nn|pp|rr|ss|tt|zz))",
                    'ei',
                    'est',
                    "est(e?)[{consonants}]{count}".format(consonants=consonants, count='{2}')
                ],
                'at_whole_word': [
                    '^est$',
                    'et'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ej': {
                'exclusions': [],
                'patterns': [
                    "eill",
                ],
                'at_whole_word': [
                    'eil$'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'œ': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    "eu" + consonants.replace('z', ''),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ø': {
                'exclusions': [],
                'patterns': [
                    "euse",
                ],
                'at_whole_word': [
                    'eu(x|t)?$'
                ],
                'space_around': [],
                'words': {}
            },
            'o': {
                'exclusions': [],
                'patterns': [
                    "eau",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɛ͂': {
                'exclusions': [],
                'patterns': [
                    "ein",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'a͂': {
                'exclusions': [],
                'patterns': [
                    "em",
                    "en",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'e': {
                'exclusions': [
                    'mer',
                    'cher',
                    'amer',
                    'hiver',
                    'fer'
                ],
                'patterns': [
                    "é"
                ],
                'at_whole_word': [
                    'er$',
                    'ez$'
                ],
                'space_at_end': [],
                'space_around': [
                    'les',
                    'des',
                    'mes',
                    'tes',
                    'ses',
                    'ces',
                    'et'
                ],
                'words': {}
            },
        },
        'è': {
            'ɛ': {
                'exclusions': [],
                'patterns': [
                    "è"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ê': {
            'ɛ': {
                'exclusions': [],
                'patterns': [
                    "ê"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'i': {
            'i': {
                'exclusions': [],
                'patterns': [
                    "i(?![aâàèêe])"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ja': {
                'exclusions': [],
                'patterns': [
                    "i(a|â|à)"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'jɛ': {
                'exclusions': [],
                'patterns': [
                    "i(è|ê|e)(?!u)"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɛ͂': {
                'exclusions': [],
                'patterns': [
                    "in",
                    "im"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'jɛ͂': {
                'exclusions': [],
                'patterns': [
                    "ien",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'jø': {
                'exclusions': [],
                'patterns': [
                    "ieuse",
                ],
                'at_whole_word': [
                    'ieu$',
                    'eux$',
                    'ieut$',
                    'ieur$',
                    'ieurs$'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ij': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    f'[{consonants}]ill'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ï': {
            'i': {
                'exclusions': [],
                'patterns': [
                    "ï"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'î': {
            'i': {
                'exclusions': [],
                'patterns': [
                    "î"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'y': {
            'i': {
                'exclusions': [],
                'patterns': [
                    "y(?![nm])"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɛ͂': {
                'exclusions': [],
                'patterns': [
                    "yn",
                    "ym"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'o': {
            'ø': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'at_whole_word': [
                    "oeu(x|t|d)?$"
                ],
                'space_around': [],
                'words': {}
            },
            'œ': {
                'exclusions': [],
                'patterns': [
                    f"oeu[{consonants}]"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'o': {
                'exclusions': [],
                'patterns': [
                    "ose"
                ],
                'at_whole_word': [
                    'o(s|p|t)?$'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɔ': {
                'exclusions': [
                    'оse'
                ],
                'at_whole_word': [],
                'patterns': [
                    f"o[{consonants}]"
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ua': {
                'exclusions': [],
                'patterns': [
                    "ou(a|â|à)",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'uɛ': {
                'exclusions': [],
                'patterns': [
                    "ou(è|ê|e)",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ui': {
                'exclusions': [],
                'patterns': [
                    "ou(i|ï|î|y)",
                ],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {}
            },
            'u': {
                'exclusions': [],
                'patterns': [
                    "ou",
                    "où"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'wa': {
                'exclusions': [],
                'patterns': [
                    "oi",
                ],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {}
            },
            'wɛ͂': {
                'exclusions': [],
                'patterns': [
                    "oin",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɔ͂': {
                'exclusions': [],
                'patterns': [
                    "on",
                    "om",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ô': {
            'o': {
                'exclusions': [],
                'patterns': [
                    "ô",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'u': {
            'y': {
                'exclusions': [
                    "qu",
                    "gu"
                ],
                'patterns': [
                    "u",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'œ͂': {
                'exclusions': [],
                'patterns': [
                    "un",
                    "um"
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ya': {
                'exclusions': [],
                'patterns': [
                    "u(a|â|à)",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'yɛ': {
                'exclusions': [],
                'patterns': [
                    "u(è|ê|e)",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'yi': {
                'exclusions': [],
                'patterns': [
                    "u(i|ï|î|y)",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'û': {
            'y': {
                'exclusions': [],
                'patterns': [
                    "û",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ü': {
            'y': {
                'exclusions': [],
                'patterns': [
                    "ü",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
    }


def english_assonance_schema():
    """
    :return: schema of vowel sounds for English language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    consonants = 'bcdfghjklmnpqrstvwxz'
    vowels = 'aeiouy'
    return {
        'a': {
            'ɒ': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'was': [[1]],
                }
            },
            'eı': {
                'exclusions': [
                    'water',
                    'was'
                ],
                'patterns': [
                    "ai",
                    "ay"
                ],
                'at_whole_word': [
                    "(?<=[{consonants}])a(?=[{consonants}][{vowels}])".format(consonants=consonants, vowels=vowels),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'eə': {
                'exclusions': [],
                'patterns': [
                    'are',
                    'air'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɔ:': {
                'exclusions': [],
                'patterns': [
                    'al',
                    'aw'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {'water': [[1]]}
            },
            'e:': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {'any': [[0]]}
            },
            'ə': {
                'exclusions': [],
                'patterns': [
                    'ar$'
                ],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'ago': [[0]],
                    'america': [[0], [6]],
                    'umbrella': [[7]],
                    'important': [[6]]
                }
            },
            'e': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'said': [[1, 2]]
                }
            },
            'a:': {
                'exclusions': [
                    'water'
                    'ago',
                    'america',
                    'umbrella',
                    'was'
                ],
                'patterns': [
                    'ar',
                    'an',
                    'a'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {'aunt': [[0, 1]]}
            },
            'æ': {
                'exclusions': [
                    'water',
                    'was',
                ],
                'patterns': [],
                'at_whole_word': [
                    "(?<=[{consonants}])a(?=[{consonants}]{count})".format(consonants=consonants, count='{1,2}')
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'e': {
            'eə': {
                'exclusions': [
                    'here',
                    'we\'re',
                    'year',
                    'hear',
                    'ear',
                    'learn'
                ],
                'patterns': [
                    'eir',
                    'ere',
                    'ear'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ɪə': {
                'exclusions': [
                    'learn'
                ],
                'patterns': [
                    'eer',
                    'ear',
                    'ere'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('ea', ['really', 'idea'])
            },
            'eı': {
                'exclusions': [
                    'bread',
                    'breakfast',
                    'meat',
                    'deal',
                    'steal',
                    'really',
                    'idea',
                    'year',
                    'hear',
                    'ear',
                    'learn'
                ],
                'patterns': [
                    'ea',
                    'ey',
                    'ei'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ə': {
                'exclusions': [],
                'patterns': [
                    'er$'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ə:': {
                'exclusions': [],
                'patterns': [
                    'er(?!$)',
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'her': [[1, 2]],
                    'learn': [[1, 2, 3]]
                }
            },
            'ı:': {
                'exclusions': [
                    'really',
                    'idea',
                    'break',
                    'steak',
                    'year',
                    'hear',
                    'ear',
                    'learn'
                ],
                'patterns': [
                    'ee',
                    'ea'
                ],
                'at_whole_word': [
                    "(?<=[{consonants}])e(?=[{consonants}][{vowels}])".format(consonants=consonants, vowels=vowels),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'people': [[1, 2]],
                    'key': [[1, 2]],
                }
            },
            'ʊə': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'euro': [[3]],
                    'europe': [[1]],
                }
            },
            'ı': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'english': [[0]],
                    'women': [[3]]
                }
            },
            'ʊ:': {
                'exclusions': [],
                'patterns': [
                    'ew'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'e': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    "(?<=[{consonants}])e(?=[{consonants}]{count})".format(consonants=consonants, count='{1,2}'),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('ea', ['breakfast', 'bread'])
            },
        },
        'i': {
            'igh': {
                'exclusions': [],
                'patterns': [
                    "igh",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'aıə': {
                'exclusions': [],
                'patterns': [
                    "ire",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ə:': {
                'exclusions': [
                    'mirrors',
                    'mirror',
                ],
                'patterns': [
                    "ir",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ı:': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'niece': [[1, 2]]
                }
            },
            'e': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'friend': [[2, 3]]
                }
            },
            'aı': {
                'exclusions': [
                    'confidence'
                    'finish'
                ],
                'at_whole_word': [
                    "(?<=[{consonants}])i(?=[{consonants}][{vowels}])".format(consonants=consonants, vowels=vowels),
                    '^i$'
                ],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'kindness': [[1]]
                }
            },
            'ı': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    "(?<=[{consonants}])i(?=[{consonants}]{count})".format(consonants=consonants, count='{1,2}'),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'o': {
            'ə': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'famous': [[3, 4]],
                    'second': [[3]],
                }
            },
            'ə:': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'work': [[1]],
                    'world': [[1, 2]],
                    'word': [[1, 2]],
                }
            },
            'ʊə': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'tourist': [[1, 2]],
                    'tour': [[1, 2]],
                    'poor': [[1, 2, 3]]
                }
            },
            'ɔ:': {
                'exclusions': [],
                'patterns': [
                    "or",
                    'ough(?=t)'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'four': [[1, 2, 3]]
                }
            },
            'ʌ': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'come': [[1]],
                    'brother': [[2]],
                    'son': [[1]],
                    'does': [[1, 2]],
                    'young': [[1, 2]]
                }
            },
            'ʊ': {
                'exclusions': [
                    'school',
                    'food',
                    'poor'
                ],
                'patterns': [
                    "oo",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'could': [[1, 2]],
                    'would': [[1, 2]],
                    'woman': [[1]]
                }
            },
            'ʊ:': {
                'exclusions': [
                    'good',
                    'book',
                    'look',
                    'room',
                    'poor'
                ],
                'patterns': [
                    "oo",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'do': [[1]],
                    'shoe': [[2, 3]]
                }
            },
            'ɔɪ': {
                'exclusions': [],
                'patterns': [
                    "oy",
                    "oi",
                ],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {}
            },
            'aʊ': {
                'exclusions': [
                    'famous',
                ],
                'patterns': [
                    "ou",
                    "ow",
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ou': {
                'exclusions': [],
                'patterns': [
                    'oa',
                    'ow'
                ],
                'at_whole_word': [
                    "(?<=[{consonants}])o(?=[{consonants}][{vowels}])".format(consonants=consonants, vowels=vowels),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'don\'t': [[1]],
                    'dont': [[1]],
                    'old': [[0]]
                }
            },
            'ɒ': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    "(?<=[{consonants}])o(?=[{consonants}]{count})".format(consonants=consonants, count='{1,2}'),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ı': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'women': [[1]]
                }
            },
        },
        'u': {
            'aı': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'buy': [[1, 2]]
                }
            },
            'ʊ': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': find_fragment_at_words('u', ['bull', 'pull', 'full', 'put'])
            },
            'ʊ:': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'june': [[1]],
                    'fruit': [[2, 3]],
                    'juice': [[1, 2]],
                }
            },
            'ʊə': {
                'exclusions': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {
                    'sure': [[1]],
                    'plural': [[2]],
                }
            },
            'ə:': {
                'exclusions': [
                    'sure',
                    'plural',
                ],
                'patterns': [
                    'ur'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ʌ': {
                'exclusions': [
                    'bull',
                    'pull',
                    'full',
                    'june',
                    'sure',
                    'plural',
                    'put'
                ],
                'patterns': [],
                'at_whole_word': [
                    "(?<=[{consonants}])u(?=[{consonants}]{count})".format(consonants=consonants, count='{1,2}'),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'juː': {
                'exclusions': [
                    'june',
                    'sure',
                    'plural',
                ],
                'patterns': [],
                'at_whole_word': [
                    "(?<=[{consonants}])u(?=[{consonants}][{vowels}])".format(consonants=consonants, vowels=vowels),
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'y': {
            'aı': {
                'exclusions': [],
                'at_whole_word': [],
                'patterns': [],
                'space_at_end': [],
                'space_around': [],
                'words': find_fragment_at_words('y', ['my', 'why'])
            },
            'ı': {
                'exclusions': [
                    'my',
                    'why'
                ],
                'patterns': [
                    'y$'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {
                    'busy': [[3]]
                }
            },
            'aıə': {
                'exclusions': [],
                'patterns': [
                    'yre'
                ],
                'space_at_end': [],
                'space_around': [],
                'at_whole_word': [],
                'words': {}
            },
        }
    }


def spanish_assonance_schema():
    """
    :return: schema of vowel sounds for Spanish language in format:
    {letter: {sound: {'exclusions': [], 'patterns': [], 'at_whole_word': [], 'space_at_end': [], 'space_around': [],
                      'words': {}, 'with_next_word': []}}
    """
    return {
        'а': {
            'aj': {
                'exclusions': [],
                'patterns': [
                    "ai",
                ],
                'at_whole_word': [
                    'hai'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'aw': {
                'exclusions': [],
                'patterns': [
                    "au",
                ],
                'at_whole_word': [
                    'hau'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'a': {
                'exclusions': [],
                'patterns': [
                    'a(?![iu])',
                ],
                'at_whole_word': [
                    'ha(?![iu])'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'á': {
            'a': {
                'exclusions': [],
                'patterns': [
                    'á'
                ],
                'at_whole_word': [
                    'há'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'е': {
            'ew': {
                'exclusions': [],
                'patterns': [
                    'еu',
                ],
                'at_whole_word': [
                    'heu'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ej': {
                'exclusions': [],
                'patterns': [
                    'ei',
                ],
                'at_whole_word': [
                    'he(?!u)'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'е': {
                'exclusions': [],
                'patterns': [
                    'е',
                ],
                'at_whole_word': [
                    'he(?!u)'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'é': {
            'е': {
                'exclusions': [],
                'patterns': [
                    'é(?!i)',
                ],
                'at_whole_word': [
                    'hé(?!i)'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'i': {
            'jaj': {
                'exclusions': [],
                'patterns': [
                    'iái',
                ],
                'at_whole_word': [
                    'hiái'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'jej': {
                'exclusions': [],
                'patterns': [
                    'iéi',
                ],
                'at_whole_word': [
                    'hiéi'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ja': {
                'exclusions': [],
                'patterns': [
                    'ia',
                ],
                'at_whole_word': [
                    'hia'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'je': {
                'exclusions': [],
                'patterns': [
                    'ie',
                ],
                'at_whole_word': [
                    'hie'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'jo': {
                'exclusions': [],
                'patterns': [
                    'io',
                ],
                'at_whole_word': [
                    'hio'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ju': {
                'exclusions': [],
                'patterns': [
                    'iu',
                ],
                'at_whole_word': [
                    'hiu'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'i': {
                'exclusions': [],
                'patterns': [
                    'i(?![eéááau])',
                ],
                'at_whole_word': [
                    'hi(?![eéáuáa])'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'í': {
            'i': {
                'exclusions': [],
                'patterns': [
                    'í(?![eéááau])',
                ],
                'at_whole_word': [
                    'hí(?![eéáuáa])'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'o': {
            'oj': {
                'exclusions': [],
                'patterns': [
                    'oi',
                ],
                'at_whole_word': [
                    'hoi'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'ow': {
                'exclusions': [],
                'patterns': [
                    'ou',
                ],
                'at_whole_word': [
                    'hou'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'o': {
                'exclusions': [],
                'patterns': [
                    'o(?![iu])',
                ],
                'at_whole_word': [
                    'ho(?![iu])'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ó': {
            'o': {
                'exclusions': [],
                'patterns': [
                    'ó',
                ],
                'at_whole_word': [
                    'hó'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            }
        },
        'q': {
            'е': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    '(?<=q)ue'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'i': {
                'exclusions': [],
                'patterns': [],
                'at_whole_word': [
                    '(?<=q)ui'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'u': {
            'waj': {
                'exclusions': [],
                'patterns': [
                    'uái',
                ],
                'at_whole_word': [
                    'huái'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'wej': {
                'exclusions': [],
                'patterns': [
                    'uéi',
                ],
                'at_whole_word': [
                    'huéi'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'uj': {
                'exclusions': [],
                'patterns': [
                    'uy',
                ],
                'at_whole_word': [
                    'huy'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'wa': {
                'exclusions': [],
                'patterns': [
                    'ua',
                    'ua'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'we': {
                'exclusions': [],
                'patterns': [
                    'ue',
                ],
                'at_whole_word': [
                    'hue'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'wi': {
                'exclusions': [],
                'patterns': [
                    'ui',
                ],
                'at_whole_word': [
                    'hui'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'wo': {
                'exclusions': [],
                'patterns': [
                    'uo',
                ],
                'at_whole_word': [
                    'huo'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
            'u': {
                'exclusions': [],
                'patterns': [
                    'u',
                ],
                'at_whole_word': [
                    'hu'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ú': {
            'u': {
                'exclusions': [],
                'patterns': [
                    'ú'
                ],
                'at_whole_word': [
                    'hú'
                ],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        },
        'ü': {
            'u': {
                'exclusions': [],
                'patterns': [
                    'ü'
                ],
                'at_whole_word': [],
                'space_at_end': [],
                'space_around': [],
                'words': {}
            },
        }
    }
