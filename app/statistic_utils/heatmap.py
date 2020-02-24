""""
ProseRhythmDetector - the tool for extraction of rhythm features.
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


decades = [1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]


def compute_mean_by_decades(feature_array, years):
    mean_features = []
    data = list(zip(feature_array, years))
    mean_feature = 0
    for decade in decades:
        features = [x for (x, year) in data if abs(decade - int(year)) <= 5]
        if len(features) < 1:
            #print(decade)
            mean_features.append(mean_feature)
        else:
            mean_feature = mean(features)
            mean_features.append(mean_feature)
    return mean_features


def create_heatmap_by_decades(data, title):
    FEATURES = data.to_numpy()
    COLUMN_NAMES = list(data.columns.values)
    years = [x[0:4] for x in list(data.index.values)]
    df = pd.DataFrame(index=decades, columns=COLUMN_NAMES)
    for i, column_name in enumerate(COLUMN_NAMES):
        feature = list(FEATURES[:, i])
        mean_features = compute_mean_by_decades(feature, years)
        df[column_name]=pd.Series(np.array(mean_features), index=decades)
    # heatmap for features
    #sn.heatmap(df, cmap="Greys")
    #plt.savefig(title + '_text-features.png', fmt='png')
    #plt.clf()
    # heatmap text-text by decades
    #transposed = df.T
    #dist_df = transposed.corr()
    metric = 'minkowski'
    df_array = df.to_numpy()    
    dist_mat = cdist(df_array, df_array, metric=metric)
    dist_df = pd.DataFrame(dist_mat, columns=decades, index=decades)
    sn.heatmap(dist_df, xticklabels=dist_df.columns, yticklabels=dist_df.columns, cmap="Greys_r", cbar=False)
    plt.savefig(title + '_' + metric + '.png', fmt='png')


if __name__ == "__main__":
    df = pd.read_csv("English.csv", header=0, index_col=0)
    plt.figure(figsize=(10, 10))
    #df = (df-df.mean())/df.std() # normalize
    create_heatmap_by_decades(df, 'en_heatmap')
