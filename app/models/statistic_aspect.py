# pylint: disable=R0903
"""
Statistic model for a specific aspect
"""


class StatisticAspect:
    """
    :var aspect: name of aspect
    :var original_count: count of specific aspect in original text
    :var translate_count: count of specific aspect in translated text
    """

    def __init__(self, aspect):
        self.aspect = aspect
        self.original_count = 0
        self.translate_count = 0
