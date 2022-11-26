import os
import sys
sys.path.insert(1, '/mnt/d/PowerTAC/Python/python_utils/helper') 

import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from statistics import mean
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots
from read_mongo_collection import HelperToReadMongo
from data_processing import DataProcessor
from network_activities import Network

import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
sns.set_theme(style="darkgrid")

from tensorflow.keras.models import load_model

helper_mongo = HelperToReadMongo()
data_processor = DataProcessor()
network = Network()

# Specify names of all the databases here
database = 'PowerTAC2021_CUP_Data_Collection'
collection1 = 'DistributionTransaction_and_Report_Info'
collection2 = 'Calendar_Info'
collection3 = 'WeatherReport_Info'

# Specify the storage path along with directory
storage_path = '/mnt/d/PowerTAC/PowerTAC2021/experiments/capacity_transaction_check/net_demand_plots/'
os.makedirs(storage_path, exist_ok=True) 

# Specify the storage path along with directory
model_storage_path = '/mnt/d/PowerTAC/PowerTAC2021/brokers/VidyutVanika21/python/models'
os.makedirs(model_storage_path, exist_ok=True) 

# Configurable Parameters
look_back = 168
look_ahead = 24
num_features = 3
    

def prepare_dataset():

    db_demand = helper_mongo.query_to_mongo(database, collection1, server_ip='192.168.0.106', ssh_username='sanjay', ssh_password='san@9397', remote=True)  
    db_cal = helper_mongo.query_to_mongo(database, collection2, server_ip='192.168.0.106', ssh_username='sanjay', ssh_password='san@9397', remote=True)  
    db_wthr = helper_mongo.query_to_mongo(database, collection3, server_ip='192.168.0.106', ssh_username='sanjay', ssh_password='san@9397', remote=True)  

    db = pd.merge(db_demand, pd.merge(db_wthr, db_cal,  how='outer', left_on=['Game_Name', 'Timeslot'], right_on = ['Game_Name', 'Timeslot']), 
                how='outer', left_on=['Game_Name', 'Timeslot'], right_on = ['Game_Name', 'Timeslot'])

    db['Hour_of_Week'] = (db['Day_of_Week']-1)*24 + db['Hour_of_Day']
    return db


def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def predict_consumption_usage(dataframe):

    try:

        features = ['Temperature', 'Wind_Speed', 'Total_Consumption']
        dataframe = dataframe[features]
        # dataframe = data_processor.onehot_encoder(dataframe, ['Hour_of_Week'])

        train, test = data_processor.train_test_split(dataframe)

        scaler = data_processor.get_scaler()
        normalized_train = data_processor.normalize_minmax(scaler, train)
        normalized_test = data_processor.normalize_minmax(scaler, test, fit = False)

        scaler_storage_path = model_storage_path + '/scalers/net_consumption.save'
        joblib.dump(scaler, scaler_storage_path)

        usage_per_population_index = list(train.columns).index('Total_Consumption')

        cols = list(dataframe.columns)
        cols.remove('Total_Consumption')
        cols.append('Total_Consumption')

        normalized_train = normalized_train[cols].values
        normalized_test = normalized_test[cols].values

        path = model_storage_path + '/Net_Consumption_Demand'
        os.makedirs(path, exist_ok=True)

        network = Network()

        train_X, train_Y = data_processor.create_lstm_dataset(normalized_train, num_features = num_features, look_back = look_back, look_ahead = look_ahead)
        test_X, test_Y = data_processor.create_lstm_dataset(normalized_test, num_features = num_features, look_back = look_back, look_ahead = look_ahead)
        model = network.create_lstm_network_2(look_back, num_features = num_features, num_labels = look_ahead)
        model = network.train_network(model, train_X, train_Y, path, validation_split = 0.20, epochs = 100, batch_size = 32, patience = 10)
        # model = load_model(path + '/best_model.hdf5')

        predicted_value= model.predict(test_X)

        reverse_scaler = data_processor.get_scaler()
        reverse_scaler.min_, reverse_scaler.scale_ = scaler.min_[usage_per_population_index], scaler.scale_[usage_per_population_index]

        predicted_test_Y = np.squeeze(reverse_scaler.inverse_transform(predicted_value))

        original_test_Y = test['Total_Consumption'][look_back:-(look_ahead-1)]
        
        fig = go.Figure([
            go.Scatter(
                name='Prediction',
                y=list(predicted_test_Y[:,0]),
                mode='lines',
            ),
            go.Scatter(
                name='Actual',
                y=original_test_Y.values.tolist(),
                mode='lines',
            )
        ])
        fig.update_layout(
            yaxis_title='Demand (MWh)',
            title='Error Plot',
            hovermode="x"
        )
        fig.write_html(path + '/error_plot.html')

        print("MAE : " + str(mean_absolute_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())))
        print("MSE : " + str(mean_squared_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())))

        mape = 0

        try:
            mape = mean_absolute_percentage_error(predicted_test_Y[:,0], original_test_Y.values.tolist())
        except Exception as e:
            print(e)

        f = open(path + '/loss.csv', 'w')
        f.write(str(mean_absolute_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())) + "," +
                str(mean_squared_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())) + "," +
                str(mape) + "\n")
        f.close()

    except Exception as e:
        print(e)


def predict_production_usage(dataframe):

    try:

        features = ['Temperature', 'Wind_Speed', 'Total_Production']
        dataframe = dataframe[features]
        # dataframe = data_processor.onehot_encoder(dataframe, ['Hour_of_Week'])

        train, test = data_processor.train_test_split(dataframe)

        scaler = data_processor.get_scaler()
        normalized_train = data_processor.normalize_minmax(scaler, train)
        normalized_test = data_processor.normalize_minmax(scaler, test, fit = False)

        scaler_storage_path = model_storage_path + '/scalers/net_production.save'
        joblib.dump(scaler, scaler_storage_path)

        usage_per_population_index = list(train.columns).index('Total_Production')

        cols = list(dataframe.columns)
        cols.remove('Total_Production')
        cols.append('Total_Production')

        normalized_train = normalized_train[cols].values
        normalized_test = normalized_test[cols].values

        path = model_storage_path + '/Net_Production_Demand'
        os.makedirs(path, exist_ok=True)

        network = Network()

        train_X, train_Y = data_processor.create_lstm_dataset(normalized_train, num_features = num_features, look_back = look_back, look_ahead = look_ahead)
        test_X, test_Y = data_processor.create_lstm_dataset(normalized_test, num_features = num_features, look_back = look_back, look_ahead = look_ahead)
        model = network.create_lstm_network_2(look_back, num_features = num_features, num_labels = look_ahead)
        model = network.train_network(model, train_X, train_Y, path, validation_split = 0.20, epochs = 100, batch_size = 32, patience = 10)
        # model = load_model(path + '/best_model.hdf5')

        predicted_value= model.predict(test_X)

        reverse_scaler = data_processor.get_scaler()
        reverse_scaler.min_, reverse_scaler.scale_ = scaler.min_[usage_per_population_index], scaler.scale_[usage_per_population_index]

        predicted_test_Y = np.squeeze(reverse_scaler.inverse_transform(predicted_value))

        original_test_Y = test['Total_Production'][look_back:-(look_ahead-1)]
        
        fig = go.Figure([
            go.Scatter(
                name='Prediction',
                y=list(predicted_test_Y[:,0]),
                mode='lines',
            ),
            go.Scatter(
                name='Actual',
                y=original_test_Y.values.tolist(),
                mode='lines',
            )
        ])
        fig.update_layout(
            yaxis_title='Demand (MWh)',
            title='Error Plot',
            hovermode="x"
        )
        fig.write_html(path + '/error_plot.html')

        print("MAE : " + str(mean_absolute_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())))
        print("MSE : " + str(mean_squared_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())))

        mape = 0

        try:
            mape = mean_absolute_percentage_error(predicted_test_Y[:,0], original_test_Y.values.tolist())
        except Exception as e:
            print(e)

        f = open(path + '/loss.csv', 'w')
        f.write(str(mean_absolute_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())) + "," +
                str(mean_squared_error(list(predicted_test_Y[:,0]), original_test_Y.values.tolist())) + "," +
                str(mape) + "\n")
        f.close()

    except Exception as e:
        print(e)



dataframe = prepare_dataset()
predict_consumption_usage(dataframe)
predict_production_usage(dataframe)
