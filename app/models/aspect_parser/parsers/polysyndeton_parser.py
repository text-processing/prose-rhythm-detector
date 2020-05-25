""" This module describes polysyndeton parser """
from itertools import chain

from models.aspect_parser.utils.conjunctions import conjunctive_adverbs, conjunctions, pair_conjunctions
from models.document import Document
from models.feature import Feature
from models.text_parser import TextParser


def __parse_simple_conjunctions_polysyndeton(sent: list, start_count: int, language: str) -> list:
    """
    :param sent: sentence as list of words
    :param start_count: position of first word in sentence in document
    :return: list of Features
    """
    res = []
    sentence = [w.lower() for w in sent]
    for conj in conjunctions(language=language):
        if sentence.count(conj) > 2:
            res.append(Feature(feature_type="polysyndeton",
                               words=[start_count + i for i, w in enumerate(sentence) if w == conj],
                               context=[start_count, start_count + len(sentence) - 1]))
    return res


def __parse_pair_conjunctions_polysyndeton(sent: list, start_count: int, language: str) -> list:
    """
    :param sent: sentence as list of words
    :param start_count: position of first word in sentence in document
    :return: list of Features
    """
    res = []
    sentence = [w.lower() for w in sent]  # <list> of words
    for conj_word_1, conj_word_2 in pair_conjunctions(language=language):
        positions = set()   # polysyndeton words positions
        first_word_met, first_word_pos = False, -1
        for i, word in enumerate(sentence):
            if word == conj_word_1:
                first_word_met, first_word_pos = True, i
            elif word == conj_word_2 and first_word_met:
                positions.update({first_word_pos, i})
                first_word_met, first_word_pos = False, -1
        if len(positions) > 2:
            res.append(Feature(feature_type="polysyndeton",
                               words=[start_count + i for i in positions],
                               context=[start_count, start_count + len(sentence) - 1]))
    return res


def __parse_conjunctive_adverbs_polysyndeton(sent: list, start_count: int, language: str) -> list:
    """
    :param sent: sentence as list of words
    :param start_count: position of first word in sentence in document
    :return: list of Features
    """
    res = []
    sentence = [w.lower() for w in sent]
    for conj_adv in conjunctive_adverbs(language=language):
        candidates_start = []  # list of start words of candidates of repeating conjuctive adverbs
        for i in range(len(sentence) - len(conj_adv) + 1):
            if tuple(sentence[i:i + len(conj_adv)]) == conj_adv:
                candidates_start.append(i)
        if len(candidates_start) > 2:
            res.append(Feature(feature_type="polysyndeton",
                               words=[start_count + c_pos + con_len for c_pos in candidates_start
                                      for con_len in range(len(conj_adv))],
                               context=[start_count, start_count + len(sentence) - 1]))
    return res


def __parse_polysyndeton(text: list, language: str) -> list:
    """
    :param text: list of chapters as list of sentences as list of words
    :param language: language of the text
    :return: list of Features
    """
    res = []
    word_count = 0
    for sent in chain.from_iterable(text):
        res.extend(__parse_simple_conjunctions_polysyndeton(sent, word_count, language))
        res.extend(__parse_pair_conjunctions_polysyndeton(sent, word_count, language))
        res.extend(__parse_conjunctive_adverbs_polysyndeton(sent, word_count, language))
        word_count += len(sent)
    return res


def parse(document: Document):
    """
           Parses polysyndeton from the specified document

       :param document: document in that will be parsing polysyndeton
       :return: list with polysyndeton (Feature objects)
       """
    words_by_sent_by_chapt = [list(map(TextParser.split_sentence_to_words, c))
                              for c in TextParser.split_text_to_sentences(document)]
    return __parse_polysyndeton(words_by_sent_by_chapt, document.language)
