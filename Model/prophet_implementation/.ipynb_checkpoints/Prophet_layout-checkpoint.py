import streamlit as st
from database.redshift import RedshiftConnection
from database.bigquery import BigqueryConnection
from prophet_implementation.Prophet_implementation import ProphetImplementation
from utility import SessionState
import pandas as pd
import plotly.express as px
ss = SessionState.get(m = None, future = None, train_data_pr=None,test_data = None, prophet_pred=None,Pred=pd.DataFrame())

def prophet_layout_implementation(vAR_method,forecast_type,bigquery):

  data=None
  if vAR_method == 'Local':
    file_upload = st.file_uploader("Choose a file",type=['csv'])
    if file_upload is not None:
      data = pd.read_csv(file_upload)
  if vAR_method == 'AWS Redshift' and forecast_type.upper()=="BOOKING":
    # data = RedshiftConnection.read_redshift_data_booking(redshift)
    st.info("Development in-progress")
  if vAR_method == 'AWS Redshift' and forecast_type.upper()=="REVENUE":
    # data = RedshiftConnection.read_redshift_data_revenue(redshift)
    st.info("Development in-progress")
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
        processed_data = None
        trained_model = None
        train_data_pr,test_data_pr,test_data = None,None,None
        prophet = ProphetImplementation()

        #Preview train data
        if vAR_preveiew_train:
          # Preview Already read data
          st.write(data)
        
        #Train model 
        if vAR_train_model and data is not None:
          bigquery = BigqueryConnection()
          truncate = BigqueryConnection.truncate_booking_table(bigquery,"PROPHET")
          st.info("Previous Data has been truncated successfully")
          ss.train_data_pr,ss.test_data_pr,ss.test_data = prophet.Datapreprocessingbooking(data)
          st.info("Data Preprocessing Completed")
          ss.m,ss.future = prophet.Model_train_booking(ss.train_data_pr,ss.test_data_pr,ss.test_data)
          st.info("Model successfully trained")
                    

        if vAR_test_data_source=='Local':
          vAR_upload_test = st.file_uploader("EXTRACT TEST DATA")
          test_data = pd.read_csv(vAR_upload_test)
          st.write(test_data)


        #Test Model
        #Keeping Trained model and X_test as session state variables
        if vAR_test_model and ss.m is not None and ss.train_data_pr is not None:
          ss.prophet_pred = prophet.predict_model_booking(ss.m,ss.future,ss.train_data_pr)
          st.info("Model Prediction Completed For Test Data")
          st.write(ss.prophet_pred)
        
        #Model outcome
        if vAR_model_outcome:
          ss.pred = prophet.process_model_outcome_booking(ss.test_data,ss.prophet_pred)
          st.write(ss.pred)
          with st.spinner("Inserting Model Outcome into bigquery"):
            BigqueryConnection.write_booking_table(bigquery,ss.pred)
          st.success("Model Outcome successfully inserted into bigquery")

        #Data Visualization
        if vAR_data_visual:
          df = pd.DataFrame()
          df["date"] = ss.pred[(ss.pred.customer_type=="FIRST TIME FLYER")]["date"]
          df["booking"] = ss.pred[(ss.pred.customer_type=="FIRST TIME FLYER")]["number_of_booking"]
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
        m = None
        future = None
        train_data_pr,test_data_pr,test_data = None,None,None
        prophet = ProphetImplementation()

        #Preview train data
        if vAR_preveiew_train:
          # Preview Already read data
          st.write(data)
        
        #Train model 
        if vAR_train_model and data is not None:
          bigquery = BigqueryConnection()
          truncate = BigqueryConnection.truncate_booking_table(bigquery,"PROPHET")
          st.info("Previous Data has been truncated successfully")
          ss.train_data_pr,ss.test_data_pr,ss.test_data = prophet.DatapreprocessingRevenue(data)
          st.info("Data Preprocessing Completed")
          ss.m,ss.future = prophet.Model_train_revenue(ss.train_data_pr,ss.test_data_pr,ss.test_data)
          st.info("Model successfully trained")
                    
        #Test Model
        #Keeping Trained model and X_test as session state variables
        if vAR_test_model and ss.m is not None and ss.train_data_pr is not None:
          ss.prophet_pred = prophet.predict_model_revenue(ss.m,ss.future,ss.train_data_pr)
          st.info("Model Prediction Completed For Test Data")
          st.write(ss.prophet_pred)
        
        #Model outcome
        if vAR_model_outcome:
          ss.pred,ss.test_data = prophet.process_model_outcome_revenue(ss.test_data,ss.prophet_pred)
          st.write(ss.pred)
          with st.spinner("Inserting Model Outcome into bigquery"):
            BigqueryConnection.write_revenue_table(bigquery,ss.pred)
          st.success("Model Outcome successfully inserted into bigquery")

        #Data Visualization
        if vAR_data_visual:
          df = pd.DataFrame()
          df["date"] = ss.model_outcome_df[(ss.model_outcome_df.customer_type=="FIRST TIME FLYER")]["date"]
          df["revenue"] = ss.model_outcome_df[(ss.model_outcome_df.customer_type=="FIRST TIME FLYER")]["revenue"]
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
