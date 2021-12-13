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

def compute_mean_by_authors(feature_array, authors, unique_authors):
    mean_features = []
    data = list(zip(feature_array, authors))
    mean_feature = 0
    for unique_author in unique_authors:
        features = [x for (x, author) in data if author == unique_author]
        mean_feature = mean(features)
        mean_features.append(mean_feature)
    return mean_features


def create_heatmap_by_authors(data, title):
    FEATURES = data.to_numpy()
    COLUMN_NAMES = list(data.columns.values)
    authors = [x.split('-')[1].strip() for x in list(data.index.values)]
    unique_authors = list(dict.fromkeys(authors))
    df = pd.DataFrame(index=unique_authors, columns=COLUMN_NAMES)
    for i, column_name in enumerate(COLUMN_NAMES):
        feature = list(FEATURES[:, i])
        mean_features = compute_mean_by_authors(feature, authors, unique_authors)
        df[column_name]=pd.Series(np.array(mean_features), index=unique_authors)
    #df = df.rename(index={'N. G. Garin_Mikhailovskij': 'N. G. Garin-Mikhailovskij', 'M. E. Saltykov_Shchedrin': 'M. E. Saltykov-Shchedrin'})
    #df = df.rename(index={'R. M. del Valle_Inclán': 'R. M. del Valle-Inclán', "A. C. Perez_Reverte":"A. C. Perez-Reverte", "L. Martin_Santos":"L. Martin-Santos", "F. Navarro_Villoslada":"F. Navarro-Villoslada"})
    plt.figure(figsize=(11, 20))
    ax = sn.heatmap(df, cbar=True, annot=True, fmt="3.1f", vmax=100)
    plt.tight_layout()
    ax.hlines([15, 40], *ax.get_xlim(), colors="white") # en
    #ax.hlines([18, 35], *ax.get_xlim(), colors="white") # ru
    #ax.hlines([12, 30], *ax.get_xlim(), colors="white") # fr
    #ax.hlines([8, 24], *ax.get_xlim(), colors="white") # es
    plt.savefig(title + '_author-features.png')
    plt.clf()

files = [
    #"rhythm_feat_ru.csv", 
    "rhythm_feat_en.csv", 
    #"rhythm_feat_fr.csv", 
    #"rhythm_feat_es.csv"
    ]


if __name__ == "__main__":
    sn.set(font_scale=1.5)
    for filename in files:
        df = pd.read_csv(filename, header=0, index_col=0)
        df = df.sort_index()
        #df_1 = df[['feat_per_sent', 'assonance', 'alliteration']]
        #create_heatmap_by_authors(df_1, 'ru_heatmap_most_frequent_features')
        df_2 = df[['lexico-grammatical features', 'polysyndeton', 'diacope', 'anaphora', 'epiphora']]*100
        df_2 = df_2.rename(columns={"lexico-grammatical features": "all"})
        create_heatmap_by_authors(df_2, filename[12:-4]+ '_heatmap_frequent_lexical_features')
        #df_3 = df[['diacope', 'polysyndeton', 'anaphora', 'epiphora']].div(df['lexical-grammatical features'], axis=0) * 100
        #create_heatmap_by_authors(df_3, filename[12:-4]+ '_heatmap_frequent_lexical_features')
