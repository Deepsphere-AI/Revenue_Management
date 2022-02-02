########################################################

#Copyright (c) DeepSphere.AI 2021

# All rights reserved

# We are sharing this partial code for learning and research, and the idea behind us sharing the source code is to stimulate ideas #and thoughts for the learners to develop their MLOps.

# Author: # DeepSphere.AI | deepsphere.ai | dsschoolofai.com | info@deepsphere.ai

# Release: Initial release

#######################################################


from sqlalchemy import create_engine
import pandas as pd
import boto3
import json

from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import numpy as np

import pandas as pd
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 



class KerasModelImplementationRevenue:
    def data_processing(self,data_frame):
        convert_dict = {'product_type' : str,
                        'customer_type' : str,
                        'date':str,
                        'year':int,
                        'quarter':str,
                        'month':str,
                        'week':int,
                        'day':str,
                        'hour':int,
                        'flight': str,
                        'origin': str,
                        'destination':str,
                        'location_lifestyle':str,
                        'location_economical_status':str,
                        'location_employment_status':str,
                        'location_event':str,
                       'revenue':float,
                        'currency':str,
                        'capacity':int,
                       'source_precipitation':str,
                        'destination_precipitation':str, 
                        'source_wind':float,
                        'destination_wind':float,
                        'source_humidity':int,
                        'destination_humidity':int,
                       'promotion':str,
                        'price_type':str}

        data_frame = data_frame.astype(convert_dict)
        df = pd.DataFrame(data_frame[['date','year','quarter','month','week','day','hour','flight','origin','destination',
                          'location_lifestyle','location_economical_status','location_employment_status','location_event',
                            'product_type','customer_type','revenue','currency','source_precipitation', 'destination_precipitation', 'source_wind','destination_wind', 'source_humidity', 'destination_humidity','promotion','price_type']].copy())
        df['origin'] = df['origin'].astype('category')
        df_source_code = dict(enumerate(df['origin'].cat.categories))
        df['destination'] = df['destination'].astype('category')
        df_destination_code = dict(enumerate(df['destination'].cat.categories))
        df['product_type'] = df['product_type'].astype('category')
        df_product_code = dict(enumerate(df['product_type'].cat.categories))
        df['customer_type'] = df['customer_type'].astype('category')
        df_product_code = dict(enumerate(df['customer_type'].cat.categories))
        df['flight'] = df['flight'].astype('category')
        df_product_code = dict(enumerate(df['flight'].cat.categories))
                
        df['location_lifestyle'] = df['location_lifestyle'].astype('category')
        df_product_code = dict(enumerate(df['location_lifestyle'].cat.categories))
        
        df['location_economical_status'] = df['location_economical_status'].astype('category')
        df_product_code = dict(enumerate(df['location_economical_status'].cat.categories))
        
        df['location_employment_status'] = df['location_employment_status'].astype('category')
        df_product_code = dict(enumerate(df['location_employment_status'].cat.categories))
        
        df['location_event'] = df['location_event'].astype('category')
        df_product_code = dict(enumerate(df['location_event'].cat.categories))
        
        df['promotion'] = df['promotion'].astype('category')
        df_product_code = dict(enumerate(df['promotion'].cat.categories))
        
        df['price_type'] = df['price_type'].astype('category')
        df_product_code = dict(enumerate(df['price_type'].cat.categories))
        
        df['quarter'] = df['quarter'].astype('category')
        df_product_code = dict(enumerate(df['quarter'].cat.categories))
        
        df['month'] = df['month'].astype('category')
        df_product_code = dict(enumerate(df['month'].cat.categories))
        
        df['day'] = df['day'].astype('category')
        df_product_code = dict(enumerate(df['day'].cat.categories))
        
        df['currency'] = df['currency'].astype('category')
        df_product_code = dict(enumerate(df['currency'].cat.categories))
        
        cat_columns = df.select_dtypes(['category']).columns
        df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
        return df
        
        
    def train_test_split(self,df):
        test_df = df.copy(deep=True)
        test_df['year'] = df['year']+1
#         df1 = df.loc[df.year == df['year'].max()]
#         df = df.loc[df.year<df['year'].max()]
        X_train = df.drop(['revenue','source_wind','destination_wind','source_precipitation','destination_precipitation','date'], axis=1)
        X_test = test_df.drop(['revenue','source_wind','destination_wind','source_precipitation','destination_precipitation','date'], axis=1)
        y_train = df["revenue"]
        y_test = test_df["revenue"]
        X_train = preprocessing.scale(X_train)

        X_test = preprocessing.scale(X_test)
        return X_train,X_test,y_train,y_test
        
    def train_model(self,X_train,y_train):
        model = Sequential()
        model.add(Dense(13, input_shape=(20,), activation = 'relu'))
        
        model.add(Dense(13, activation='relu'))
        model.add(Dense(13, activation='relu'))
        model.add(Dense(13, activation='relu'))
        model.add(Dense(13, activation='relu'))
        
        model.add(Dense(1,))
        model.compile(Adam(lr=0.01), 'mean_squared_error',metrics=['accuracy'])
        history = model.fit(X_train, y_train, epochs = 20, validation_split = 0.1,verbose = 0)
        return model
        
    def predict_model(self,model,X_test):
        y_test_pred = model.predict(X_test)
        print(y_test_pred)
        return y_test_pred
    
    def process_model_outcome(self,data_frame,y_test_pred):
#         data_frame = data_frame.drop(['date'],axis=1)
#         data_frame = data_frame.loc[data_frame.year == data_frame['year'].max()]
        row_count = data_frame.shape[0]
        accuracy_list = list(np.random.random_sample((row_count,)))
        prob_list = list(np.random.random_sample((row_count,)))
        data_frame['year'] = data_frame['year'].astype(int)+1
        data_frame['date'] = data_frame['date'] + pd.offsets.DateOffset(years=1)
        data_frame['date'] = data_frame['date'].astype(str)
        data_frame['data_category'] = 'FORECAST'
        data_frame['data_source'] = 'MODEL'
        data_frame['model_name'] = 'KERAS'
        # data_frame['created_by'] = username
        data_frame['created_at'] = pd.Timestamp.now()
        data_frame['created_at'] = data_frame['created_at'].astype(str)
        # Needs to be changed accuracy&probability
        data_frame['model_accuracy'] = "0"
        data_frame['accuracy_probability'] = "0%"
        # data_frame['date'] = str(data_frame['year'])+'-'+str(data_frame['month'])+'-'+str(data_frame['day'])+' '+str(data_frame['hour'])+':00:00'
        test_data = data_frame.drop(['revenue'], axis=1)
        data_frame['revenue'] = y_test_pred.astype(float)
        data_frame['model_accuracy'] = [round(num, 2) for num in accuracy_list]
        data_frame['model_accuracy'] = data_frame['model_accuracy'].astype(str)
        data_frame['accuracy_probability'] = [round(num, 2) for num in prob_list]
        data_frame['accuracy_probability'] = data_frame['accuracy_probability'].astype(str)
        #Add date,booking,model_accuracy,model_prob
        print("len(test_data)",len(test_data))
        return data_frame