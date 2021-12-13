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


def rename_genre(genre):
    if genre == 'ad':
        return 'Реклама'
    if genre == 'novels':
        return 'Романы'
    if genre == 'polit':
        return 'Полит. статьи'
    if genre == 'reviews':
        return 'Отзывы'
    if genre == 'science':
        return 'Науч. статьи'
    if genre == 'tw':
        return 'Твиты'


lang = "ru"
csv_filenames = [
    lang + "_ad_rhythm.csv",
    lang + "_novels_rhythm.csv",
    lang + "_polit_rhythm.csv",
    lang + "_reviews_rhythm.csv",
    lang + "_science_articles_rhythm.csv",
    lang + "_tw_rhythm.csv",
                 ]

dataframe_list = []

for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    #df = df*100 # Привести значения в диапазон, в котором их легче интерпретировать
    genre = filename.split('_')[1].strip()
    df['genre'] = [rename_genre(genre)] * len(df)
    dataframe_list.append(df)

df = pd.concat(dataframe_list)
plt.figure(figsize=(10, 10))
#features = ['feat_per_sent', 'anaphora','epiphora','symploce','anadiplosis','diacope','epizeuxis','epanalepsis','chiasmus','polysyndeton','repeating exclamatory sentences','repeating interrogative sentences','assonance','alliteration','aposiopesis', 'lexico-grammatical features']
features = ['lexico-grammatical features']
#features = ['anaphora','epiphora','symploce','anadiplosis','diacope','epizeuxis','epanalepsis','chiasmus','polysyndeton','exclamatory','interrogative', 'aposiopesis', 'lexico-grammatical features']
sn.set(font_scale=1.5)
for feature in features:
    sn.boxplot(orient="h", x=feature, y="genre", data=df,  showmeans=True, meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"10"}).set(xlabel='Количество лексико-грамматических средств на одно предложение', ylabel='Жанр')
    plt.tight_layout()
    plt.savefig(feature.replace(' ', '_') + '_boxplot-' + lang + '.png')
    plt.clf()
