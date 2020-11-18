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

import seaborn as sn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from scipy.spatial.distance import cdist


decades = [
    #1810, 
    1820,
    1830, 1840, 1850, 1860, 1870, 1880, 1890,1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010
           ]


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
            print(decade, len(features))
            mean_feature = mean(features)
            mean_features.append(mean_feature)
    return mean_features


def create_heatmap_by_decades(data, title, does_construct_heatmap_of_similarity, does_construct_heatmap_of_feature_values):
    FEATURES = data.to_numpy()
    COLUMN_NAMES = list(data.columns.values)
    years = [x[0:4] for x in list(data.index.values)]
    df = pd.DataFrame(index=decades, columns=COLUMN_NAMES)
    for i, column_name in enumerate(COLUMN_NAMES):
        feature = list(FEATURES[:, i])
        mean_features = compute_mean_by_decades(feature, years)
        df[column_name]=pd.Series(np.array(mean_features), index=decades)
    plt.figure(figsize=(10, 10))
    if does_construct_heatmap_of_similarity:
        # heatmap text-text by decades
        #metric = 'chebyshev'
        metric = 'correlation'
        df_array = df.to_numpy()
        dist_mat = cdist(df_array, df_array, metric=metric)
        dist_df = pd.DataFrame(dist_mat, columns=decades, index=decades)
        sn.heatmap(dist_df, xticklabels=dist_df.columns, yticklabels=dist_df.columns, cbar=False)
        plt.savefig(title + '_' + metric + '.png')
        plt.clf()
    if does_construct_heatmap_of_feature_values:
        # heatmap for features
        sn.heatmap(df, cbar=True, annot=True, fmt="3.1f", cmap="YlGnBu") #Greys
        plt.tight_layout()
        plt.savefig(title + '_text-features.png')


if __name__ == "__main__":
    sn.set(font_scale=1.5)
    df = pd.read_csv("rhythm_feat_fr.csv", header=0, index_col=0)
    df.drop(["NOUN", "ADJS", "VERB", "ADVB", "feat_per_sent", "one_word", "assonance", "alliteration"], axis = 1, inplace = True) # Можно удалить столбцы, чтобы не учитывать их
    create_heatmap_by_decades(df*100, 'ru_heatmap_tendencies', False, True)
    df = df.div(df['lexical-grammatical features'], axis=0) * 100
    df.drop(["lexical-grammatical features"], axis = 1, inplace = True)
    #df = (df-df.mean())/df.std() # Нормализовать значения для подсчёта близости
    #df.drop(["number_of_sentence", "average_sentence_length_by_character", "average_sentence_length_by_word", "average_word_length"], axis = 1, inplace = True)
    create_heatmap_by_decades(df, 'fr_heatmap_percentage', False, True)
