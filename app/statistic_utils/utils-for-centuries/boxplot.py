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

df = pd.read_csv("rhythm_feat_fr.csv", header=0, index_col=0)
df = df*100 # Привести значения в диапазон, в котором их легче интерпретировать
df['decade'] = [(int(x.split('-')[0].strip())//10)*10 for x in list(df.index.values)]
plt.figure(figsize=(10, 10))
#features = ['feat_per_sent', 'anaphora','epiphora','symploce','anadiplosis','diacope','epizeuxis','epanalepsis','chiasmus','polysyndeton','repeating exclamatory sentences','repeating interrogative sentences','assonance','alliteration','aposiopesis', 'lexical-grammatical features']
#features = ['lexical-grammatical features']
features = ['anaphora','epiphora','symploce','anadiplosis','diacope','epizeuxis','epanalepsis','chiasmus','polysyndeton','repeating exclamatory sentences','repeating interrogative sentences', 'aposiopesis', 'lexical-grammatical features']
sn.set(font_scale=1.5)
for feature in features:
    sn.boxplot(orient="h", x=feature, y="decade", data=df,  showmeans=True, meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"10"})
    plt.tight_layout()
    plt.savefig(feature.replace(' ', '_') + '_boxplot-fr.png')
    plt.clf()
