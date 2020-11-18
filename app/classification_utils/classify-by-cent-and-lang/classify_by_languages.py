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

from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import pandas as pd
import numpy as np

csv_filenames = ["char_and_word.csv", "all_rhythm.csv", "all_features.csv"]
result_file = open('ml_lang_norm.txt', "w")
for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    y = df['language']
    df.drop(columns=['language'], inplace=True)
    df = (df-df.mean())/df.std()
    X = df.to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 100)
    classifiers = [AdaBoostClassifier(n_estimators=50, random_state=100),
                   RandomForestClassifier(n_estimators=50, max_depth=3, random_state=100)]
    result_file.write(filename + '\n')
    for classifier in classifiers:
        result_file.write(str(classifier) + '\n')
        model = classifier.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = model.score(X_test, y_test)
        result_file.write(str(round(accuracy * 100, 1)) + ' & ')
        precision = precision_score(y_test, predictions, average='macro') * 100
        result_file.write(str(round(precision, 1))  + ' & ')
        recall = recall_score(y_test, predictions, average='macro') * 100
        result_file.write(str(round(recall, 1))  + ' & ')
        f_measure = 2 * precision * recall / (precision + recall)
        result_file.write(str(round(f_measure, 1)) + '\n')
        result_file.write('\n')
result_file.close()
