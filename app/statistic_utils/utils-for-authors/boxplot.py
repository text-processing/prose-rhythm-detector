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
import matplotlib.pyplot as plt

files = ["en_rhythm_stat.csv", "ru_rhythm_stat.csv", "es_rhythm_stat.csv", "fr_rhythm_stat.csv"]
for filename in files:
    df = pd.read_csv(filename, header=0, index_col=0)
    df = df*100 # Привести значения в диапазон, в котором их легче интерпретировать
    df['max_word_distance'] = df['max_word_distance'] /100 #вернуть нормальный диапазон
    df['avg_word_distance'] = df['avg_word_distance'] /100 #вернуть нормальный диапазон
    features = df.columns
    df['author'] = [x.split('-')[1].strip() for x in list(df.index.values)]
    plt.figure(figsize=(10, 10))
    #features = ['feat_per_sent', 'anaphora','epiphora','symploce','anadiplosis','diacope','epizeuxis','epanalepsis','chiasmus','polysyndeton','repeating exclamatory sentences','repeating interrogative sentences','assonance','alliteration','aposiopesis', 'lexico-grammatical features']
    #features = ['lexico-grammatical features']
    colors = ['#FFFFFF', '#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080', '#696969']
    sn.set(font_scale=1.5)
    for feature in features:
        sn.boxplot(orient="h", x=feature, y="author", data=df,  showmeans=True, palette=sn.color_palette(colors), meanprops={"marker":"o",
                                                                                                                             "markerfacecolor":"white", 
                                                                                                                             "markeredgecolor":"black",
                                                                                                                             "markersize":"10"})
        plt.tight_layout()
        plt.savefig('boxplots/' + filename[:2] + '_' + feature.replace(' ', '_') + '_boxplot' + '.png')
        plt.clf()
