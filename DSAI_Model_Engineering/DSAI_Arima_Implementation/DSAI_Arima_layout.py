########################################################

#Copyright (c) DeepSphere.AI 2021

# All rights reserved

# We are sharing this partial code for learning and research, and the idea behind us sharing the source code is to stimulate ideas #and thoughts for the learners to develop their MLOps.

# Author: # DeepSphere.AI | deepsphere.ai | dsschoolofai.com | info@deepsphere.ai

# Release: Initial release

#######################################################


import streamlit as st
from database.redshift import RedshiftConnection
from database.bigquery import BigqueryConnection
from arima_implementation.Arima_implementation import ArimaImplementation
from utility import SessionState
import pandas as pd
import plotly.express as px
ss = SessionState.get(trained_model = None, data1 =None, arima_pred=None,Pred=pd.DataFrame())


def arima_layout_implementation(vAR_method,forecast_type,bigquery):

  data=None
  if vAR_method == 'Local':
    file_upload = st.file_uploader("Choose a file",type=['csv'])
    if file_upload is not None:
      data = pd.read_csv(file_upload)
  if vAR_method == 'AWS Redshift' and forecast_type.upper()=="BOOKING":
    st.info("Development in-progress")
    # data = RedshiftConnection.read_redshift_data_booking(redshift)
  if vAR_method == 'AWS Redshift' and forecast_type.upper()=="REVENUE":
    st.info("Development in-progress")
    # data = RedshiftConnection.read_redshift_data_revenue(redshift)
  if vAR_method == 'Google Drive':
    st.info("Development in-progress")
  if vAR_method == 'Google Bigquery'  and forecast_type.upper()=="BOOKING":
    data = BigqueryConnection.read_booking_table(bigquery)
  if vAR_method == 'Google Bigquery'  and forecast_type.upper()=="REVENUE":
    data = BigqueryConnection.read_revenue_table(bigquery)
  if vAR_method == 'MySQL':
    st.info("Development in-progress")
  if vAR_method == 'Web Scrap':
    st.info("Development in-progress")
 


  if data is not None:
    cols = data.columns
    _, col = st.columns([3,1])
    with _:
      with st.expander("DATA PREVIEW"):
        st.write(data)
  # For page breaks, The columns are reassigned
    col2, col3,_ = st.columns([3,3,1])
    with col3:
      with col2:
            st.write('')
            st.write('')             
            st.subheader("Feature selection")
      vAR_features = st.multiselect('',cols)
    _, col2 = st.columns([3,1])
    with _:
            st.write('')
            st.write('')
            with st.expander("List selected features"):
              for i in range(0,len(vAR_features)):
                st.write('Feature',i+1,':',vAR_features[i])


    col2, col3,_ = st.columns([3,3,1])
    with col2:
      st.subheader("Hyper Parameter Tuning")
      for i in range(22):
        st.write('')
      st.subheader("Extract Test Data")
    with col3:
      vAR_epoch = st.text_input('Epochs')
      vAR_learning_rate = st.text_input('Learning_rate')
      vAR_dimension = st.text_input('Dimension')
      vAR_preveiew_train = st.button("PREVIEW TRAIN DATA")
      vAR_train_model = st.button("TRAIN MODEL")
      vAR_test_data_source = st.selectbox('',('Select the method', 'Local','AWS Redshift','Google Drive','Google Bigquery','MySQL','Web Scrap'),index=0,key="123")
      vAR_preview_test_data = st.button("PREVIEW TEST DATA")
      vAR_test_model = st.button("TEST MODEL")
      vAR_model_outcome = st.button("REVIEW MODEL OUTCOME")
      vAR_data_visual = st.button("DATA VISUALIZATION/ANALYSIS")


    if forecast_type.upper()=="BOOKING":
      
      _, col = st.columns([3,1])
      with _:
        arima_result = None
        trained_model = None
        arima = ArimaImplementation()

        #Preview train data
        if vAR_preveiew_train:
          # Preview Already read data
          st.write(data)
        
        #Train model 
        if vAR_train_model and data is not None:
          bigquery = BigqueryConnection()
          truncate = BigqueryConnection.truncate_booking_table(bigquery,"ARIMA")
          st.info("Previous Data has been truncated successfully")
          ss.data1 = arima.Datapreprocessing(data)
          st.info("Data Preprocessing Completed")
          ss.arima_result,ss.test_data,ss.train_data = arima.Model_train_booking(ss.data1)
          st.info("Model successfully trained")
                    

        if vAR_test_data_source=='Local':
          vAR_upload_test = st.file_uploader("EXTRACT TEST DATA")
          test_data = pd.read_csv(vAR_upload_test)
          st.write(test_data)

        #Test Model
        #Keeping Trained model and X_test as session state variables
        if vAR_test_model and ss.arima_result is not None and ss.test_data is not None:
          ss.arima_pred = arima.predict_model_booking(ss.arima_result,ss.test_data,ss.data1)
          st.info("Model Prediction Completed For Test Data")
          st.write(ss.arima_pred)
        
        #Model outcome
        if vAR_model_outcome:
          ss.Pred,ss.test_data = arima.process_model_outcome_booking(ss.arima_pred,ss.train_data)
          print("###########",type(ss.Pred))
          st.write(ss.Pred)
          with st.spinner("Inserting Model Outcome into Bigquery"):
              BigqueryConnection.write_booking_table(bigquery,ss.Pred)
          st.success("Model Outcome successfully inserted into bigquery")

        #Data Visualization
        if vAR_data_visual:
          df = pd.DataFrame()
          df["date"] = ss.Pred[(ss.Pred.customer_type=="FIRST TIME FLYER")]["date"]
          df["booking"] = ss.Pred[(ss.Pred.customer_type=="FIRST TIME FLYER")]["number_of_booking"]
          # df = df.rename(columns={'date':'index'}).set_index('index')
          # st.line_chart(df)
          #The plot
          fig = px.line(        
                  df, #Data Frame
                  x = "date", #Columns from the data frame
                  y = "booking",
                  title = "Forecasting Number of Booking"
              )
          fig.update_traces(line_color = "blue")
          st.plotly_chart(fig)

    elif forecast_type.upper()=="REVENUE":
      _, col = st.columns([3,1])
      with _:
        processed_data = None
        trained_model = None
        arima = ArimaImplementation()

        #Preview train data
        if vAR_preveiew_train:
          # Preview Already read data
          st.write(data)
        
        #Train model 
        if vAR_train_model and data is not None:
          bigquery = BigqueryConnection()
          truncate = BigqueryConnection.truncate_booking_table(bigquery,"ARIMA")
          st.info("Previous Data has been truncated successfully")
          ss.data1 = arima.Datapreprocessing(data)
          st.info("Data Preprocessing Completed")
          ss.train_data,ss.arima_result,ss.test_data = arima.Model_train_revenue(ss.data1)
          st.info("Model successfully trained")
                    
        #Test Model
        #Keeping Trained model and X_test as session state variables
        if vAR_test_model and ss.arima_result is not None and ss.train_data is not None:
          ss.arima_pred = arima.predict_model_revenue(ss.arima_result,ss.train_data,ss.data1)
          st.info("Model Prediction Completed For Test Data")
          st.write(ss.arima_pred)
        
        #Model outcome
        if vAR_model_outcome:
          bigquery = BigqueryConnection()
          ss.Pred,ss.test_data = arima.process_model_outcome_revenue(ss.arima_pred,ss.test_data)
          st.write(ss.Pred)
          with st.spinner("Inserting Model Outcome into Redshift"):
            BigqueryConnection.write_revenue_table(bigquery,ss.Pred)
          st.success("Model Outcome successfully inserted into redshift")

        #Data Visualization
        if vAR_data_visual:
          df = pd.DataFrame()
          df["date"] = ss.Pred[(ss.Pred.customer_type=="FIRST TIME FLYER")]["date"]
          df["revenue"] = ss.Pred[(ss.Pred.customer_type=="FIRST TIME FLYER")]["revenue"]
          # df = df.rename(columns={'Date':'index'}).set_index('index')
          # st.line_chart(df)
          #The plot
          fig = px.line(        
                  df, #Data Frame
                  x = "date", #Columns from the data frame
                  y = "revenue",
                  title = "Forecasting Revenue"
              )
          fig.update_traces(line_color = "blue")
          st.plotly_chart(fig)
