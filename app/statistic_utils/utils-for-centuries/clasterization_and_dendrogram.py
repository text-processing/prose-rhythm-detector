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
Cluster texts by the k-means method to 3 clasters and by creating the dendrogram.

Output files contain the plot with dendrogram and the list of clusters with texts.

Run this utility:

python3 clasterization_and_dendrogram.py -f FEATURES_FILE -o OUTPUT_DIR

-f FEATURES_FILE, --features=FEATURES_FILE:
\tPath to a file with feature vectors for texts.
-o OUTPUT_DIR, --output=OUTPUT_DIR:
\tThe output directory for clustering data.
-h, --help:
\tPrints help of the script.
"""

import itertools
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.cluster import hierarchy
import pandas as pd
import numpy as np
from user_interface import get_arguments, save_plot
from statistics import mean


HELP_TEXT = """Usage: python3 statistic-utils/clasterization_and_dendrogram.py -f FEATURES_FILE -o OUTPUT_DIR
-f FEATURES_FILE, --features=FEATURES_FILE:
\tPath to a file with feature vectors for texts.
-o OUTPUT_DIR, --output=OUTPUT_DIR:
\tThe output directory for clustering data.
-h, --help:
\tPrints help of the script.
"""


def create_dendrogram_by_method_and_metric(data, text_name, output_dir, method, metric):
    """ Create a dendrogram and save it to output_dir with the filemame text_name + '_dendrogram' """
    features = data.to_numpy()
    plt.figure(figsize=(15, 10))
    plt.title("Dendogram")
    hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
    hierarchy.dendrogram(hierarchy.linkage(features, method=method, metric=metric), labels=list(data.index.values))
    save_plot(text_name + '_dendrogram, method = ' + method + ', metric = ' + metric, output_dir)
    plt.clf()


def create_dendrograms(data, text_name, output_dir):
    """ Create dendrograms for data with different methods and metrics"""
    methods = ['single', 'complete', 'average']
    metrics = ['braycurtis', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'minkowski']
    for method in methods:
        for metric in metrics:
            create_dendrogram_by_method_and_metric(data, text_name, output_dir, method, metric)
    methods = ['centroid', 'median', 'ward']
    for method in methods:
        create_dendrogram_by_method_and_metric(data, text_name, output_dir, method, 'euclidean')


def cluster_texts_with_kmeans(data):
    """ Cluster the data to three clusters with the kmeans algorithm"""
    texts_names = list(data.index.values)
    kmeans = KMeans(n_clusters=2, random_state=42).fit(data)
    return zip(kmeans.labels_, texts_names)


decades = [
    1810, 1820,
    1830, 1840, 1850, 1860, 1870, 1880, 1890,1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010
           ]


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


if __name__ == "__main__":
    FEATURES_FILE, OUTPUT = get_arguments(HELP_TEXT)
    data = pd.read_csv(FEATURES_FILE, header=0, index_col=0)
    data = (data-data.mean())/data.std()
    FEATURES = data.to_numpy()
    COLUMN_NAMES = list(data.columns.values)
    years = [x[0:4] for x in list(data.index.values)]
    df = pd.DataFrame(index=decades, columns=COLUMN_NAMES)
    for i, column_name in enumerate(COLUMN_NAMES):
        feature = list(FEATURES[:, i])
        mean_features = compute_mean_by_decades(feature, years)
        df[column_name]=pd.Series(np.array(mean_features), index=decades)
    CLUSTERS = sorted(cluster_texts_with_kmeans(df), key=lambda x: x[0])
    CLUSTERED_DATA = itertools.groupby(CLUSTERS, key=lambda x: x[0])
    create_dendrograms(df, FEATURES_FILE[:-4], OUTPUT)
    with open(OUTPUT + '/' + FEATURES_FILE[:-4] + "_clusters.txt", "w") as f:
        for key, grp in CLUSTERED_DATA:
            f.write('{}: {}'.format(key, [x[1] for x in grp]))
            f.write('\n')
