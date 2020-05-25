""" This module describes context intersection between two Features """

from models.feature import Feature


def context_intersection(first: Feature, second: Feature) -> list:
    """
    Returns context intersection between two features

    :param first: first feature
    :param second: second feature
    :return: context intersection
    """
    first_beg, first_end = first.context_begin(), first.context_end()
    second_beg, second_end = second.context_begin(), second.context_end()
    if first_beg > second_end or second_beg > first_end:
        return []
    return [max(first_beg, second_beg), min(first_end, second_end)]
