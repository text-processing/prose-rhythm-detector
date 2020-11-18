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
from keras.models import Sequential
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, Bidirectional, GRU
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from keras import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_fscore_support

def get_century_by_year(year):
    if 1800 < year <= 1850:
        return 0
    elif 1850 < year <= 1900:
        return 1
    elif 1900 < year <= 1950:
        return 2
    elif 1950 < year <= 2000:
        return 3
    else:
        return 4


def baseline_model():
    input_number = df.shape[1] - 1
    model = Sequential()
    model.add(GRU(4, input_shape=(1, input_number)))
    model.add(Dense(5, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


csv_filenames = ["all_char_fr.csv", "all_word_fr.csv", "all_rhythm_fr.csv", "all_char_and_rhythm_fr.csv", "all_char_and_word_fr.csv", "all_word_and_rhythm_fr.csv",
    "all_features_fr.csv"]
result_file = open('net_century_half_GRU_1.txt', "w")
for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    df = (df-df.mean())/df.std()
    df.insert(0, 'ID', range(0, 0 + len(df)))
    X = df.to_numpy()
    y = []
    for year in [int(x[0:4]) for x in list(df.index.values)]:
        y.append(get_century_by_year(year))
    one_hot_y = np_utils.to_categorical(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, one_hot_y, random_state = 55)
    ids = X_test[:,0] # Сохраняем идентификаторы тестовых данных, чтобы потом анализировать ошибки
    X_train = np.delete(X_train, 0, axis=1)
    X_test = np.delete(X_test, 0, axis=1)
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1])) # для LSTM и GRU
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
    model = baseline_model()
    model.fit(X_train, y_train, epochs=100, batch_size=5, verbose=0)
    test_loss, test_acc = model.evaluate(X_test, y_test)
    predictions = model.predict(X_test)
    result_file.write(filename + '\n')
    macro = precision_recall_fscore_support(np.argmax(y_test, axis=1), np.argmax(predictions, axis=1), average='macro')
    precision = macro[0] * 100
    recall = macro[1] * 100
    f_measure = 2 * precision * recall / (precision + recall)
    result_file.write(str(round(test_acc * 100, 1)) + ' & ' + str(round(precision, 1))  + ' & ' + str(round(recall, 1))  + ' & ' + str(round(f_measure, 1)) + '\n')
    result_file.write('\n')
result_file.close()

