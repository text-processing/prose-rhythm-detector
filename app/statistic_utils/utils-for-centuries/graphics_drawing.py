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

"""
Creates plots for stylometric features of texts.

Output png files contain plots for each stylometric feature.

Run this utility:

python3 graphics_drawing.py -f FEATURES_FILE -o OUTPUT_DIR

-f FEATURES_FILE, --features=FEATURES_FILE:
\tPath to a file with feature vectors for texts.
-o OUTPUT_DIR, --output=OUTPUT_DIR:
\tThe output directory for images with plots.
-h, --help:
\tPrints help of the script.
"""

import matplotlib.pyplot as plt
import pandas as pd
from user_interface import get_arguments, save_plot
from statsmodels.nonparametric.smoothers_lowess import lowess
from statistics import mean


HELP_TEXT = """Usage: python3 graphics_drawing.py -f FEATURES_FILE -o OUTPUT_DIR
-f FEATURES_FILE, --features=FEATURES_FILE:
\tPath to a file with feature vectors for texts.
-o OUTPUT_DIR, --output=OUTPUT_DIR:
\tThe output directory for images with plots.
-h, --help:
\tPrints help of the script.
"""


decades = [
    #1810, 1820, 
    1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]


def compute_mean_by_decades(feature_array, years):
    mean_features = []
    data = list(zip(feature_array, years))
    mean_feature = 0
    for decade in decades:
        features = [x for (x, year) in data if 0 <= int(year) - decade <= 9]
        if len(features) < 1:
            print(decade)
            mean_features.append(mean_feature)
        else:
            mean_feature = mean(features)
            mean_features.append(mean_feature)
    return mean_features


def create_plot_by_decades(data, title, OUTPUT):
    FEATURES = data.to_numpy()
    COLUMN_NAMES = list(data.columns.values)
    years = [x[0:4] for x in list(data.index.values)]
    plt.figure(figsize=(7, 7))
    plt.locator_params(axis='x', nbins=len(decades))
    #plt.title(title)
    plt.xlabel('time periods')
    plt.ylabel('figures per 100 sentences')
    line_types = ['-k', '--k', '-.k', ':k']
    for i, name in enumerate(COLUMN_NAMES):
        feature = list(FEATURES[:, i])
        filtered = lowess(compute_mean_by_decades(feature, years), decades, frac=1./2)
        if name == 'feat_per_sent':
            name = 'all figures'
        elif name == 'one_word':
            name = 'hapax legomenon'
        plt.plot(decades, filtered[:, 1], line_types[i], label=name)
    plt.legend()
    save_plot(title, OUTPUT)
    plt.clf()


def create_plot_by_separate_texts(DATA, title, OUTPUT):
    FEATURES = DATA.to_numpy()
    COLUMN_NAMES = list(DATA.columns.values)
    years = [x[0:-4] for x in list(DATA.index.values)]
    plt.figure(figsize=(60, 10))
    plt.locator_params(axis='x', nbins=len(years))
    line_types = ['-k', '--k', '-.k', ':k']
    for i, name in enumerate(COLUMN_NAMES):
        feature = list(FEATURES[:, i])
        #feature = lowess(feature, years, frac=1./2)
        if name == 'feat_per_sent':
            name = 'all figures'
        elif name == 'one_word':
            name = 'hapax legomenon'
        elif name == 'NOUN':
            name = 'nouns'
        elif name == 'ADJS':
            name = 'adjectives'
        elif name == 'VERB':
            name = 'verbs'
        elif name == 'ADVB':
            name = 'adverbs'
        plt.plot(years, feature, line_types[i], label=name)
    plt.tick_params(axis ='x', rotation = 90)
    plt.tight_layout()
    plt.legend()
    save_plot(title, OUTPUT)
    plt.clf()


if __name__ == "__main__":
    FEATURES_FILE, OUTPUT = get_arguments(HELP_TEXT)
    DATA = pd.read_csv(FEATURES_FILE, header=0, index_col=0)
    DATA = DATA * 100
    DATA.sort_index(inplace=True)
    MAIN_TENDENCIES = DATA[['diacope', 'polysyndeton', 'lexical-grammatical features']]
    SMALL_TENDENCIES = DATA[['anaphora', 'epiphora', 'epizeuxis']]
    #BIG_TENDENCIES = DATA[['feat_per_sent', 'alliteration', 'assonance']]
    create_plot_by_decades(MAIN_TENDENCIES, 'rhythm_features_lexical_' + FEATURES_FILE[:-4], OUTPUT)
    create_plot_by_decades(SMALL_TENDENCIES, 'rhythm_features_anaphora_' + FEATURES_FILE[:-4], OUTPUT)
    #create_plot_by_decades(BIG_TENDENCIES, 'rhythm_features_all_' + FEATURES_FILE[:-4], OUTPUT)
