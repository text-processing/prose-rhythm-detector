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

import pandas
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, Bidirectional, GRU
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from tensorflow.keras import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def baseline_model():
    input_number = df.shape[1]
    model = Sequential()
    model.add(Bidirectional(LSTM(64), input_shape=(1, input_number)))
    #model.add(GRU(4, input_shape=(1, input_number)))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


csv_filenames = ["es_rhythm_no_sums.csv", "fr_rhythm_no_sums.csv", "en_rhythm_no_sums.csv", "ru_rhythm_no_sums.csv"]
result_file = open('verification_biLSTM.txt', "w")


def verify_author(df):
    result_file.write('Verify ' + author + '\n')
    y = [0 if label == author else 1 for label in classes_labels]
    result_file.write('Number of fragments: ' + str(len(y) - sum(y)) + '\n')
    #verify_once(y, df)
    f1 = cross_validate(y, df)
    result_file.write('\n')
    return f1


def cross_validate(y, df):
    X = df.to_numpy()
    result_file.write("Cross-validation\n")
    X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
    estimator = KerasClassifier(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)
    print("Precision")
    results = cross_val_score(estimator, X, y, cv=KFold(n_splits=5, shuffle=True), scoring='precision_macro')
    precision = results.mean() * 100
    precision_variability = results.std() * 100
    print("Recall")
    results = cross_val_score(estimator, X, y, cv=KFold(n_splits=5, shuffle=True), scoring='recall_macro')
    recall = results.mean() * 100
    recall_variability = results.std() * 100
    print("F1")
    results = cross_val_score(estimator, X, y, cv=KFold(n_splits=5, shuffle=True), scoring='f1_macro')
    f_measure = results.mean() * 100
    f_measure_variability = results.std() * 100
    precisions.append(precision)
    recalls.append(recall)
    result_file.write(author + ' & ' + str(round(precision, 1)) + ' & ' + str(round(precision_variability, 1)) +
                      ' & ' + str(round(recall, 1)) + ' & ' + str(round(recall_variability, 1)) +
                      ' & ' + str(round(f_measure, 1)) + ' & ' + str(round(f_measure_variability, 1)) + '\n')
    return f_measure
    


def verify_once(y, df):
    one_hot_y = to_categorical(y)
    df = (df - df.mean()) / df.std()
    df.insert(0, 'ID', range(0, 0 + len(df)))
    X = df.to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, one_hot_y, random_state=55)
    ids = X_test[:, 0]  # Сохраняем идентификаторы тестовых данных, чтобы потом анализировать ошибки
    X_train = np.delete(X_train, 0, axis=1)
    X_test = np.delete(X_test, 0, axis=1)
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))  # для LSTM и GRU
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
    model = baseline_model()
    model.fit(X_train, y_train, epochs=100, batch_size=5, verbose=0)
    predictions = model.predict(X_test)
    macro = precision_recall_fscore_support(np.argmax(y_test, axis=1), np.argmax(predictions, axis=1), average='macro')
    precision = macro[0] * 100
    recall = macro[1] * 100
    f_measure = 2 * precision * recall / (precision + recall)
    precisions.append(precision)
    recalls.append(recall)
    result_file.write(author + ' & ' + str(round(precision, 1)) + ' & ' + str(round(recall, 1)) + ' & ' + str(
        round(f_measure, 1)) + '\n')
    for text_id, prediction, real in zip(ids, np.argmax(predictions, axis=1), np.argmax(y_test, axis=1)):
        text_name = df.index.values[int(text_id)]
        if real != prediction:
            result_file.write(text_name + ' ' + str(prediction) + '\n')


for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    result_file.write(filename + '\n')
    
    classes_labels = [index.split('-')[1].strip() for index, row in df.iterrows()]
    unique_classes = set(classes_labels)
    result_file.write(str(unique_classes) + '\n')

    precisions = []
    recalls = []
    df_mean = pd.read_csv(filename[0:2] + "_frequent_lexical_features_mean_by_authors.csv", header=0, index_col=0)
    df_mean['f1'] = 0
    for author in unique_classes:
        print(author)
        f1 = verify_author(df)
        df_mean.at[author,'f1'] = f1
    result_file.write('Average metrics\n')
    mean_precision = sum(precisions) / len(precisions)
    result_file.write(str(round(mean_precision, 1)) + ' & ')
    mean_recall = sum(recalls) / len(recalls)
    result_file.write(str(round(mean_recall, 1)) + ' & ')
    mean_f_measure = 2 * mean_precision * mean_recall / (mean_precision + mean_recall)
    result_file.write(str(round(mean_f_measure, 1)) + '\n')
    result_file.write('\n')
    df_mean.to_csv(filename[0:2] + "_frequent_lexical_features_mean_by_authors_with_f1.csv")
result_file.close()
