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
from sklearn.model_selection import cross_validate
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


lang = "ru"
csv_filenames = [
    #"tmp.csv"
    "ru_science_articles_rhythm_no_sums.csv"
    #lang + "_char.csv",
    #lang + "_word.csv", lang + "_rhythm.csv",
                 ##lang + "_char_and_word.csv", lang + "_char_and_rhythm.csv", 
                 ##lang + "_word_and_rhythm.csv",
                 #lang + "_all_features.csv"
                 ]
result_file = open('AdaBoost_verification_with_pca_'+ lang+'.txt', "w")


def getFeatureTypeByFilename(filename):
    if "_all_features" in filename:
        return "7-All"
    elif "_word_and_rhythm" in filename:
        return "6-W + Rh"
    elif "_char_and_rhythm" in filename:
        return "5-Ch + Rh"
    elif "_char_and_word" in filename:
        return "4-Ch + W"
    elif "_rhythm" in filename:
        return "3-Rh"
    elif "_word" in filename:
        return "2-W"
    else:
        return "1-Ch"


def cross_val(filename):
    #classifier = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=100)
    classifier = AdaBoostClassifier(n_estimators=50, random_state=100)
    results = cross_validate(classifier, X, y, cv=KFold(n_splits=5, shuffle=True), scoring=['precision_macro', 'recall_macro', 'f1_macro'])
    precision = results['test_precision_macro'].mean() * 100
    precision_variability = results['test_precision_macro'].std() * 100
    recall = results['test_recall_macro'].mean() * 100
    recall_variability = results['test_recall_macro'].std() * 100
    f_measure = results['test_f1_macro'].mean() * 100
    f_measure_variability = results['test_f1_macro'].std() * 100
    precisions.append(precision)
    recalls.append(recall)
    result_file.write(author + ' & ' + getFeatureTypeByFilename(filename) + ' & ' + str(round(precision, 1)) + ' & ' + str(round(precision_variability, 1)) +
                      ' & ' + str(round(recall, 1)) + ' & ' + str(round(recall_variability, 1)) +
                      ' & ' + str(round(f_measure, 1)) + ' & ' + str(round(f_measure_variability, 1)) + ' \\\\ \n')


for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    result_file.write(filename + '\n')
    
    classes_labels = [index.split('-')[1].strip() for index, row in df.iterrows()]
    unique_classes = set(classes_labels)
    result_file.write(str(unique_classes) + '\n')
    
    #df = df.drop(columns=['B', 'C'])    
    
    #df = (df-df.mean())/df.std()
    df = df.dropna()
    #print(df)
    X = df.to_numpy()
    #print(X)
    #quit()
    
    #X = StandardScaler().fit_transform(df)
    #if filename == lang + "_rhythm.csv":
        #n_components = len(df.columns) - 5
    #elif filename == lang + "_all_features.csv":
        #n_components=len(df.columns) - 25
    #else:
        #n_components=len(df.columns) - 10
    #pca = PCA(n_components=n_components)
    #X = pca.fit_transform(X)

    precisions = []
    recalls = []
    for author in unique_classes:
        print(author)
        #result_file.write('Verify ' + author + '\n')
        y = [0 if label == author else 1 for label in classes_labels]
        #result_file.write('Number of fragments: ' + str(len(y) - sum(y)) + '\n')
        cross_val(filename)
        #result_file.write('\n')
    result_file.write('Average metrics\n' + getFeatureTypeByFilename(filename) + ' & ')
    mean_precision = sum(precisions) / len(precisions)
    result_file.write(str(round(mean_precision, 1)) + ' & ')
    mean_recall = sum(recalls) / len(recalls)
    result_file.write(str(round(mean_recall, 1)) + ' & ')
    mean_f_measure = 2 * mean_precision * mean_recall / (mean_precision + mean_recall)
    result_file.write(str(round(mean_f_measure, 1)) + '\n')
    result_file.write('\n')
result_file.close()
