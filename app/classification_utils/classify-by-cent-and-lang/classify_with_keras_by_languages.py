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

def baseline_model():
    input_number = df.shape[1]
    model = Sequential()
    model.add(GRU(4, input_shape=(1, input_number)))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


csv_filenames = ["char_and_word.csv", "all_rhythm.csv", "all_features.csv"]
result_file = open('net_lang_gru.txt', "w")
for filename in csv_filenames:
    df = pd.read_csv(filename, header=0, index_col=0)
    y = df['language']
    df.drop(columns=['language'], inplace=True)
    df = (df-df.mean())/df.std()
    X = df.to_numpy()
    one_hot_y = np_utils.to_categorical(y)
    result_file.write(filename + '\n')
    X_train, X_test, y_train, y_test = train_test_split(X, one_hot_y, random_state = 55)
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
    model = baseline_model()
    model.fit(X_train, y_train, epochs=50, batch_size=5, verbose=0)
    test_loss, test_acc = model.evaluate(X_test, y_test)
    predictions = model.predict(X_test)
    macro = precision_recall_fscore_support(np.argmax(y_test, axis=1), np.argmax(predictions, axis=1), average='macro')
    precision = macro[0] * 100
    recall = macro[1] * 100
    f_measure = 2 * precision * recall / (precision + recall)
    result_file.write(str(round(test_acc * 100, 1)) + ' & ' + str(round(precision, 1))  + ' & ' + str(round(recall, 1))  + ' & ' + str(round(f_measure, 1)) + '\n')
    result_file.write('\n')
result_file.close()

