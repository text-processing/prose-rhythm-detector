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

def create_heatmap(data, title):
    plt.figure(figsize=(15, 12))
    sn.heatmap(data, cbar=True, annot=True, fmt="3.2f", vmax=1.0).set(ylabel='Жанры')
    plt.yticks(rotation=0, va="center")
    plt.tight_layout()
    plt.savefig(title + '.png')
    plt.clf()

files = [
    "en_mean_values.csv",
    "ru_mean_values.csv"
    ]


if __name__ == "__main__":
    sn.set(font_scale=1.5)
    for filename in files:
        df = pd.read_csv(filename, header=0, index_col=0)
        df_1 = df[['lexico-grammatical features', 'diacope', 'polysyndeton', 'anaphora']]
        df_1 = df_1.rename(columns={"lexico-grammatical features": "Лексико-грамматические средства", "diacope": "Диакопа", 'polysyndeton':"Многосоюзие", 'anaphora': 'Анафора'})
        create_heatmap(df_1, filename[:-4] + '_heatmap_features')
