""" This module describes symploce parser """
from models.aspect_parser.utils.context_intersection import context_intersection
from models.feature import Feature


def parse(anaphoras: list, epistrophas: list) -> list:
    """
    Parses symploce from the specified document

    :param anaphoras: list with anaphoras
    :param epistrophas: list with epistrophas
    :return: list with epistrophe (Feature objects)
    """
    res = list()
    for anaphora in anaphoras:
        for epistrophe in epistrophas:
            intersection = context_intersection(anaphora, epistrophe)
            if intersection:
                inter_start, inter_end = intersection
                anaphora_words = [word for word in anaphora.words() if inter_start <= word <= inter_end]
                epistrophe_words = [word for word in epistrophe.words() if inter_start <= word <= inter_end]
                if anaphora_words and epistrophe_words:
                    if anaphora_words[-1] > epistrophe_words[0]:
                        res.append(Feature("symploce", words=sorted(anaphora_words + epistrophe_words),
                                           context=intersection))
    return res
