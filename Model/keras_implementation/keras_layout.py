import streamlit as st
from database.redshift import RedshiftConnection
from database.bigquery import BigqueryConnection
from keras_implementation.keras_impl_booking import KerasModelImplementationBooking
from keras_implementation.keras_impl_revenue import KerasModelImplementationRevenue
from utility import SessionState
import pandas as pd
import plotly.express as px
ss = SessionState.get(trained_model = None,X_test=None,y_test_pred=None,model_outcome_df=pd.DataFrame())

def common_layout():
    st.markdown("""
    <hr style="width:100%;height:3px;background-color:gray;border-width:10">
    """, unsafe_allow_html=True)
    col2, col3,_ = st.columns([3,3,1])
    with col2:
        
        st.write('')
        st.write('')
        st.subheader("Forecasting Target")
        st.write('')
        st.write('')
        st.subheader("Forecasting Period")
        st.write('')
        st.write('')
        st.subheader("Problem Type")
        st.write('')
        st.write('')
        st.subheader("Model Selection")
        st.write('')
        st.write('')
        st.subheader("Extract Training Data")
        st.write('')
        st.write('')

    with col3:
        vAR_target = st.selectbox('',('Select the field', 'Booking', 'Revenue'),index=0)
        vAR_period = st.selectbox('',('Select the forecast period', 'Rolling Forecast(6 months)', 'Annual Forecast(12 months)'),index=0)
        vAR_problem_type = st.selectbox('',('Select Problem Type','Regression','Classification','Clustering','Time Series Forecasting'),index=0)
        vAR_model = st.selectbox('',('Select the model', 'Keras', 'ARIMA', 'DeepAR','Prophet','Amazon Forecast'),index=0)
        vAR_method = st.selectbox('',('Select the method', 'Local','AWS Redshift','Google Drive','Google Bigquery','MySQL','Web Scrap'),index=0)
        
        return vAR_model,vAR_target,vAR_period,vAR_method,vAR_problem_type



def keras_layout_implementation(vAR_method,forecast_type,bigquery):
  # aws_access_key,aws_secret_key = get_gcp_secret()
  # secret = get_aws_secret(aws_access_key,aws_secret_key)
  # username = secret['username']
  # password = secret['password']
  # engine = secret['engine']
  # host = secret['host']
  # port = secret['port']
  # redshift = RedshiftConnection(username,password,engine,host,port)
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
        processed_data = None
        trained_model = None
        X_test,X_train,y_test,y_train = None,None,None,None
        keras = KerasModelImplementationBooking()

        #Preview train data
        if vAR_preveiew_train:
          # Preview Already read data
          st.write(data)
        
        #Train model 
        if vAR_train_model and data is not None:
          bigquery = BigqueryConnection()
          truncate = BigqueryConnection.truncate_booking_table(bigquery,"KERAS")
          st.info("Previous Data has been truncated successfully")
          processed_data = keras.data_processing(data)
          st.info("Data Preprocessing Completed")
          X_train,ss.X_test,y_train,y_test = keras.train_test_split(processed_data)
          st.info("Test, Train data splitted")
          ss.trained_model = keras.train_model(X_train,y_train)
          st.info("Model successfully trained")
                    

        if vAR_test_data_source=='Local':
          vAR_upload_test = st.file_uploader("EXTRACT TEST DATA")
          test_data = pd.read_csv(vAR_upload_test)
          st.write(test_data)


        #Test Model
        #Keeping Trained model and X_test as session state variables
        if vAR_test_model and ss.trained_model is not None and ss.X_test is not None:
          ss.y_test_pred = keras.predict_model(ss.trained_model,ss.X_test)
          st.info("Model Prediction Completed For Test Data")
          st.write(ss.X_test)
        
        #Model outcome
        if vAR_model_outcome:
          bigquery = BigqueryConnection()
          ss.model_outcome_df = keras.process_model_outcome(data,ss.y_test_pred)
          st.write(ss.model_outcome_df)
          with st.spinner("Inserting Model Outcome into Bigquery"):
            BigqueryConnection.write_booking_table(bigquery,ss.model_outcome_df)
          st.success("Model Outcome successfully inserted into Bigquery")

        #Data Visualization
        if vAR_data_visual:
          df = pd.DataFrame()
          df["date"] = ss.model_outcome_df[(ss.model_outcome_df.customer_type=="FIRST TIME FLYER")]["date"]
          df["booking"] = ss.model_outcome_df[(ss.model_outcome_df.customer_type=="FIRST TIME FLYER")]["number_of_booking"]
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
        X_test,X_train,y_test,y_train = None,None,None,None
        keras = KerasModelImplementationRevenue()

        #Preview train data
        if vAR_preveiew_train:
          # Preview Already read data
          st.write(data)
        
        #Train model 
        if vAR_train_model and data is not None:
          bigquery = BigqueryConnection()
          truncate = BigqueryConnection.truncate_revenue_table(bigquery,"KERAS")
          st.info("Previous Data has been truncated successfully")
          processed_data = keras.data_processing(data)
          st.info("Data Preprocessing Completed")
          X_train,ss.X_test,y_train,y_test = keras.train_test_split(processed_data)
          st.info("Test, Train data splitted")
          ss.trained_model = keras.train_model(X_train,y_train)
          st.info("Model successfully trained")
                    
        #Test Model
        #Keeping Trained model and X_test as session state variables
        if vAR_test_model and ss.trained_model is not None and ss.X_test is not None:
          ss.y_test_pred = keras.predict_model(ss.trained_model,ss.X_test)
          st.info("Model Prediction Completed For Test Data")
          st.write(ss.X_test)
        
        #Model outcome
        if vAR_model_outcome:
          bigquery = BigqueryConnection()
          ss.model_outcome_df = keras.process_model_outcome(data,ss.y_test_pred)
          st.write(ss.model_outcome_df)
          with st.spinner("Inserting Model Outcome into Bigquery"):
            BigqueryConnection.write_revenue_table(bigquery,ss.model_outcome_df)
          st.success("Model Outcome successfully inserted into Bigquery")

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

