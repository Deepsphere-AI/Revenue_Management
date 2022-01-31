from database.redshift import RedshiftConnection,get_aws_secret,get_gcp_secret
import html
import streamlit as st
import streamlit.components.v1 as cmpnts
from PIL import Image
import pandas as pd
from utility.utility import local_css,all_initialization
from keras_implementation.keras_layout import common_layout,keras_layout_implementation
from arima_implementation.Arima_layout import arima_layout_implementation
from prophet_implementation.Prophet_layout import prophet_layout_implementation
import traceback
import sys
from database.bigquery import BigqueryConnection



if __name__ == '__main__':
    st.set_page_config(page_title="MLOps Framework")
    try:
        local_css("utility/style.css")
        model_choice = all_initialization()

        if model_choice=='Home':
            vAR_model,vAR_target,vAR_period,vAR_method,vAR_problem_type = common_layout()
            bigquery = BigqueryConnection()
            booking_forecast_type = "BOOKING"
            revenue_forecast_type = "REVENUE"
            if vAR_problem_type=='Time Series Forecasting':
                if vAR_model=='Keras':
                    if vAR_target=='Booking':
                        keras_layout_implementation(vAR_method,booking_forecast_type,bigquery)
                    if vAR_target=='Revenue':
                        keras_layout_implementation(vAR_method,revenue_forecast_type,bigquery)
                if vAR_model=='ARIMA':
                    if vAR_target=='Booking':
                        arima_layout_implementation(vAR_method,booking_forecast_type,bigquery)
                    if vAR_target=='Revenue':
                        arima_layout_implementation(vAR_method,revenue_forecast_type,bigquery)
                if vAR_model=='DeepAR':
                    if vAR_target=='Booking':
                        pass
                    if vAR_target=='Revenue':
                        pass
                if vAR_model=='Prophet':
                    if vAR_target=='Booking':
                        prophet_layout_implementation(vAR_method,booking_forecast_type,bigquery)
                    if vAR_target=='Revenue':
                        prophet_layout_implementation(vAR_method,revenue_forecast_type,bigquery)
                if vAR_model=='Amazon Forecast':
                    if vAR_target=='Booking':
                        pass
                    if vAR_target=='Revenue':
                        pass

        else:
            st.write('')
            st.write('')
            st.info('Development in-progress')

    except BaseException as e:
        st.error('In Error block - '+str(e))
        traceback.print_exception(*sys.exc_info())

        