# pylint: disable=R0903
"""
Statistic controller
"""

from models.statistic_aspect import StatisticAspect


class StatisticController:
    """
    Controller that manipulate with statistic
    """

    def __init__(self):
        self.aspects = {}

    def form_aspect_statistic(self, feature_list_original):
        """
        Form statistic for every aspect from feature lists
        :param feature_list_original: list of features of original text
        :param feature_list_translate: list of features of translated text
        """
        self.aspects = {}
        for feature in feature_list_original:
            if feature.type not in self.aspects:
                self.aspects[feature.type] = StatisticAspect(feature.type)
            self.aspects[feature.type].original_count = self.aspects[feature.type].original_count + 1
