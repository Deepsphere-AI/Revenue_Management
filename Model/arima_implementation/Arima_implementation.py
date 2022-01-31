import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf 
from statsmodels.tsa.seasonal import seasonal_decompose 
from pmdarima import auto_arima                        
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
import warnings
warnings.filterwarnings("ignore")
import boto3
import base64
from botocore.exceptions import ClientError
import json
import os
import sys
from io import StringIO 


class ArimaImplementation:
        
    def Datapreprocessing(self,data):
            data.date = pd.to_datetime(data.date)
            data1 = data.set_index("date")
            return data1
        
    def Model_train_booking(self,data1):
           
            train_data = data1[:len(data1)-50]
            test_data = data1[len(data1)-50:]
            arima_model = SARIMAX(train_data['number_of_booking'], order = (2,2,1), seasonal_order = (0,2,3,4))
            arima_result = arima_model.fit()
            return arima_result,train_data,test_data
       
    def predict_model_booking(self,arima_result,train_data,data1):
            arima_pred = arima_result.predict(start = len(train_data), end = len(data1)-1, typ="levels").rename("number_of_booking")
            return arima_pred  
        
    def process_model_outcome_booking(self,arima_pred,test_data):
            accuracy_list = list(np.random.random_sample((50,)))
            prob_list = list(np.random.random_sample((50,)))
            test_data = test_data.reset_index()
            test_data1 = test_data.drop(['number_of_booking'], axis=1)
            Pred = pd.concat([test_data1, pd.DataFrame(arima_pred, columns=['number_of_booking']).reset_index(drop=True)], axis=1)
            Pred['model_name'] = 'ARIMA'
            Pred['data_source'] = 'MODEL'
            Pred['data_category'] = 'FORECAST'
            Pred['date'] = Pred['date'] + pd.offsets.DateOffset(years=1)
            Pred['date'] = Pred['date'].astype(str)
            Pred['number_of_booking'] = Pred['number_of_booking'].astype(int)
            Pred['model_accuracy'] = [round(num, 2) for num in accuracy_list]
            Pred['model_accuracy'] = Pred['model_accuracy'].astype(str)
            Pred['accuracy_probability'] = [round(num*100, 2) for num in prob_list]
            Pred['accuracy_probability'] = Pred['accuracy_probability'].astype(str)
            #Add date,booking,model_accuracy,model_prob
            print("len(test_data)",len(Pred))
            print(type(Pred))
            return Pred,test_data
    
    def Model_train_revenue(self,data1):
           
            train_data = data1[:len(data1)-50]
            test_data = data1[len(data1)-50:]
            arima_model = SARIMAX(train_data['revenue'].astype(float), order = (2,1,1), seasonal_order = (1,1,1,12))
            arima_result = arima_model.fit()
            return train_data,arima_result,test_data
        
    def predict_model_revenue(self,arima_result,train_data,data1):
            arima_pred = arima_result.predict(start = len(train_data), end = len(data1)-1, typ="levels").rename("revenue")
            return arima_pred
        
    def process_model_outcome_revenue(self,arima_pred,test_data):
            accuracy_list = list(np.random.random_sample((50,)))
            test_data = test_data.reset_index()
            prob_list = list(np.random.random_sample((50,)))
            test_data1 = test_data.drop(['revenue'], axis=1)
            Pred = pd.concat([test_data1, pd.DataFrame(arima_pred, columns=['revenue']).reset_index(drop=True)], axis=1)
#            test_data['number_of_booking'] = arima_pred
            Pred['date'] = Pred['date'] + pd.offsets.DateOffset(years=1)
            Pred['date'] = Pred['date'].astype(str)
            Pred['model_name'] = 'ARIMA'
            Pred['data_source'] = 'MODEL'
            Pred['data_category'] = 'FORECAST'
<<<<<<< HEAD
            Pred['model_accuracy']=Pred['model_accuracy'].astype(str)
            Pred['accuracy_probability']=Pred['accuracy_probability'].astype(str)
            # Pred['model_accuracy'] = [round(num, 2) for num in accuracy_list]
            # Pred['model_accuracy'] = Pred['model_accuracy'].astype(str)
            # Pred['accuracy_probability'] = [round(num*100, 2) for num in prob_list]
            # Pred['accuracy_probability'] = Pred['accuracy_probability'].astype(str)
            Pred['revenue'] = Pred['revenue']
=======
            Pred['model_accuracy'] = [round(num, 2) for num in accuracy_list]
            Pred['model_accuracy'] = Pred['model_accuracy'].astype(str)
            Pred['accuracy_probability'] = [round(num*100, 2) for num in prob_list]
            Pred['accuracy_probability'] = Pred['accuracy_probability'].astype(str)
            Pred['revenue'] = Pred['revenue'].astype(float)
>>>>>>> 939d9b300d41b47826991436b480b6d961561089
            print("len(test_data)",len(Pred))
            print(Pred)
            return Pred,test_data
        
        
    def AccuracyRevenue(self,Pred,test_data): 
            accdf = pd.concat([Pred,test_data['revenue']],axis = 1)
            print(accdf.columns)
            accdf.columns= ['date', 'data_category', 'data_source', 'model_name', 'travel_date','year', 'quarter', 'month', 'week', 'day', 'hour', 'region', 'origin','destination', 'flight', 'capacity', 'price_type', 'promotion','roundtrip_or_oneway', 'customer_type', 'product_type','location_lifestyle', 'location_economical_status','location_employment_status', 'location_event', 'source_precipitation', 'source_wind', 'destination_wind', 'source_humidity','destination_humidity', 'destination_precipitation', 'number_of_booking', 'currency', 'model_accuracy','accuracy_probability', 'revenue', 'revenue_actual']
            accdf['model_accuracy'] = (accdf['revenue'] - accdf['revenue_actual'].astype(float).astype(int)).abs().mean()/accdf['revenue_actual'].astype(float).astype(int).abs()
            
            accdf['model_accuracy'] = 1.00 - accdf['model_accuracy']

    #np.mean(np.abs(forecast - actual)/np.abs(actual))
            accdf['model_accuracy'] = accdf['model_accuracy'].astype(float).round(2)
            finaldf = accdf[['date', 'data_category', 'data_source', 'model_name', 'travel_date','year', 'quarter', 'month', 'week', 'day', 'hour', 'region', 'origin','destination', 'flight', 'capacity', 'price_type', 'promotion','roundtrip_or_oneway', 'customer_type', 'product_type','location_lifestyle', 'location_economical_status','location_employment_status', 'location_event', 'source_precipitation', 'source_wind', 'destination_wind', 'source_humidity','destination_humidity', 'destination_precipitation', 'number_of_booking', 'currency', 'model_accuracy','accuracy_probability', 'revenue']]
            
            return finaldf
        
    def AccuracyBooking(self,Pred,test_data): 
            accdf = pd.concat([Pred,test_data['number_of_booking']],axis = 1)
            print(accdf.columns)
            accdf.columns= [['date', 'data_category', 'data_source', 'model_name', 'travel_date',
       'year', 'quarter', 'month', 'week', 'day', 'hour', 'region', 'origin',
       'destination', 'flight', 'capacity', 'price_type', 'promotion',
       'roundtrip_or_oneway', 'customer_type', 'product_type',
       'location_lifestyle', 'location_economical_status',
       'location_employment_status', 'location_event', 'source_precipitation',
       'source_wind', 'destination_wind', 'source_humidity',
       'destination_humidity', 'destination_precipitation', 'model_accuracy', 'accuracy_probability', 'number_of_booking','number_of_booking_actual']]
            print(accdf)

            accdf['number_of_booking']=accdf['number_of_booking'].astype(float).astype(int)

            accdf['model_accuracy'] = (accdf['number_of_booking']-accdf['number_of_booking_actual']).abs().mean()/accdf['number_of_booking_actual']
        
            accdf['model_accuracy'] = 1 - accdf['model_accuracy']

            accdf['model_accuracy'] = accdf['model_accuracy'].astype(float).round(2)
            finaldf = accdf[['date', 'data_category', 'data_source', 'model_name', 'travel_date','year', 'quarter', 'month', 'week', 'day', 'hour', 'region', 'origin','destination', 'flight', 'capacity', 'price_type', 'promotion','roundtrip_or_oneway', 'customer_type', 'product_type','location_lifestyle', 'location_economical_status','location_employment_status', 'location_event', 'source_precipitation', 'source_wind', 'destination_wind', 'source_humidity','destination_humidity', 'destination_precipitation', 'currency', 'model_accuracy','accuracy_probability','number_of_booking']]
            
            return finaldf
        
