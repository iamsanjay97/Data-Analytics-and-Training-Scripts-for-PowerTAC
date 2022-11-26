from __future__ import print_function

from read_mongo_collection import HelperToReadMongo
from data_processing import DataProcessor
from network_activities import Network

from hyperopt import Trials, STATUS_OK, tpe, rand
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import accuracy_score
from hyperas import optim
from hyperas.distributions import choice, uniform
from keras import optimizers

import numpy as np
import matplotlib.pyplot as plt

def data():

    helper_to_read_mongo = HelperToReadMongo()

    collection = helper_to_read_mongo.get_collection('PowerTAC2019_Wholesale', 'Individual Cleared Trade Record')
    dtype = np.dtype([('Proximity', np.int64), ('Day of Week', np.int64), ('Hour of Day', np.int64), ('Temperature', np.double), ('Wind Spped', np.double), ('Wind Direction', np.double), ('Cloud Speed', np.double), ('MCP', np.double), ('Net Cleared Quantity', np.double)])
    dataframe = helper_to_read_mongo.convert_collection_to_dataframe(collection, dtype)

    data_processor = DataProcessor()

    num_features = 60
    num_labels = 1

    df_encoded = data_processor.onehot_encoder(dataframe, ['Proximity', 'Day of Week', 'Hour of Day'])
    df_encoded = data_processor.shuffle_samples(df_encoded)
    train, validate, test = data_processor.train_validate_test_split(df_encoded)

    scaler = data_processor.get_scaler()
    normalized_train = data_processor.normalize_minmax(scaler, train)
    normalized_validate = data_processor.normalize_minmax(scaler, validate)
    normalized_test = data_processor.normalize_minmax(scaler, test)

    train_X = normalized_train.loc[:, normalized_train.columns != 'MCP']
    train_Y = normalized_train['MCP']

    validate_X = normalized_validate.loc[:, normalized_validate.columns != 'MCP']
    validate_Y = normalized_validate['MCP']

    test_X = normalized_test.loc[:, normalized_test.columns != 'MCP']
    test_Y = normalized_test['MCP']

    return train_X, validate_X, test_X, train_Y, validate_Y, test_Y, scaler, num_features, num_labels


def create_model(train_X, train_Y, validate_X, validate_Y, num_features, num_labels):

    model = Sequential()
    model.add(Dense({{choice([np.power(2, 5), np.power(2, 6), np.power(2, 7)])}}, input_shape=(num_features,)))
    model.add(LeakyReLU(alpha={{uniform(0.5, 1)}}))
    model.add(Dropout({{uniform(0.5, 1)}}))
    model.add(Dense({{choice([np.power(2, 3), np.power(2, 4), np.power(2, 5)])}}))
    model.add(LeakyReLU(alpha={{uniform(0.5, 1)}}))
    model.add(Dropout({{uniform(0.5, 1)}}))
    model.add(Dense({{choice([np.power(2, 3), np.power(2, 4), np.power(2, 5)])}}))
    model.add(LeakyReLU(alpha={{uniform(0.5, 1)}}))
    model.add(Dropout({{uniform(0.5, 1)}}))
    model.add(Dense(num_labels, activation='sigmoid'))

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=25, min_lr=0.001)

    model.compile(optimizer={{choice(['rmsprop', 'adam', 'sgd'])}}, loss='mse', metrics=['accuracy'])

    model.fit(train_X, train_Y, epochs={{choice([50, 75, 100, 500, 1000, 5000])}}, batch_size={{choice([16, 32, 64, 128, 256])}}, validation_data=(validate_X, validate_Y), callbacks=[reduce_lr])

    score, acc = model.evaluate(validate_X, validate_Y, verbose=0)
    print('Test accuracy:', acc)
    return {'loss': -acc, 'status': STATUS_OK, 'model': model}

if __name__ == '__main__':

    best_run, best_model = optim.minimize(model=create_model, data=data, algo=tpe.suggest, max_evals=15, trials=Trials())
    train_X, validate_X, test_X, train_Y, validate_Y, test_Y, scaler, num_features, num_labels = data()
    print("Evalutation of best performing model:")
    print(best_model.evaluate(test_X, test_Y))
    print("Best performing model chosen hyper-parameters:")
    print(best_run)
    best_model.save('best_model.h5')
