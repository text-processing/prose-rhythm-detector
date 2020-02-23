""" This module describes merging two or more Features """

from itertools import chain

from models.feature import Feature


def merge_features(*features) -> Feature:
    """
    Merges two or more Features of one type into one

    :param features: list of features to merge
    :returns: Feature
    """
    feature_type = features[0].type()
    context_start = min(feature.context_begin() for feature in features)
    context_end = max(feature.context_end() for feature in features)
    words = sorted(chain.from_iterable(diac.words() for diac in features))
    return Feature(feature_type=feature_type, context=[context_start, context_end], words=words)
