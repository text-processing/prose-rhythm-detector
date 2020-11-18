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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np

csv_filenames = ["es_rhythm_no_sums.csv", "fr_rhythm_no_sums.csv", "en_rhythm_no_sums.csv", "ru_rhythm_no_sums.csv"]
result_file = open('RandomForest_verification.txt', "w")


def verify_once():
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=100)
    # classifier = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=100)
    classifier = AdaBoostClassifier(n_estimators=50, random_state=100)
    result_file.write(str(classifier) + '\n')
    model = classifier.fit(X_train, y_train)
    predictions = model.predict(X_test)
    precision = precision_score(y_test, predictions, average='macro') * 100
    precisions.append(precision)
    result_file.write(str(round(precision, 1)) + ' & ')
    recall = recall_score(y_test, predictions, average='macro') * 100
    recalls.append(recall)
    result_file.write(str(round(recall, 1)) + ' & ')
    f_measure = 2 * precision * recall / (precision + recall)
    result_file.write(str(round(f_measure, 1)) + '\n')


def cross_validate():
    result_file.write("Cross-validation\n")
    classifier = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=100)
    #classifier = AdaBoostClassifier(n_estimators=50, random_state=100)
    results = cross_val_score(classifier, X, y, cv=KFold(n_splits=5, shuffle=True), scoring='precision_macro')
    precision = results.mean() * 100
    precision_variability = results.std() * 100
    results = cross_val_score(classifier, X, y, cv=KFold(n_splits=5, shuffle=True), scoring='recall_macro')
    recall = results.mean() * 100
    recall_variability = results.std() * 100
    results = cross_val_score(classifier, X, y, cv=KFold(n_splits=5, shuffle=True), scoring='f1_macro')
    f_measure = results.mean() * 100
    f_measure_variability = results.std() * 100
    precisions.append(precision)
    recalls.append(recall)
    result_file.write(author + ' & ' + str(round(precision, 1)) + ' & ' + str(round(precision_variability, 1)) +
                      ' & ' + str(round(recall, 1)) + ' & ' + str(round(recall_variability, 1)) +
                      ' & ' + str(round(f_measure, 1)) + ' & ' + str(round(f_measure_variability, 1)) + '\n')


for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    result_file.write(filename + '\n')
    
    classes_labels = [index.split('-')[1].strip() for index, row in df.iterrows()]
    unique_classes = set(classes_labels)
    result_file.write(str(unique_classes) + '\n')
    
    df = (df-df.mean())/df.std()
    X = df.to_numpy()

    precisions = []
    recalls = []
    for author in unique_classes:
        print(author)
        result_file.write('Verify ' + author + '\n')
        y = [0 if label == author else 1 for label in classes_labels]
        result_file.write('Number of fragments: ' + str(len(y) - sum(y)) + '\n')
        #verify_once()
        cross_validate()
        result_file.write('\n')
    result_file.write('Average metrics\n')
    mean_precision = sum(precisions) / len(precisions)
    result_file.write(str(round(mean_precision, 1)) + ' & ')
    mean_recall = sum(recalls) / len(recalls)
    result_file.write(str(round(mean_recall, 1)) + ' & ')
    mean_f_measure = 2 * mean_precision * mean_recall / (mean_precision + mean_recall)
    result_file.write(str(round(mean_f_measure, 1)) + '\n')
    result_file.write('\n')
result_file.close()
