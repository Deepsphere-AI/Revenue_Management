########################################################

#Copyright (c) DeepSphere.AI 2021

# All rights reserved

# We are sharing this partial code for learning and research, and the idea behind us sharing the source code is to stimulate ideas #and thoughts for the learners to develop their MLOps.

# Author: # DeepSphere.AI | deepsphere.ai | dsschoolofai.com | info@deepsphere.ai

# Release: Initial release

#######################################################



import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def all_initialization():
    col1, col2,col3 = st.columns(3)
    with col3:
      st.image("logo/aws_logo.jpg",width=200)
    with col1:
        st.image('logo/Logo_final.png',width=230)
    with col2:
        st.image('logo/gcp_logo.png',width=200)

    st.markdown("<h1 style='text-align: center; color: blue; font-size:32px;'>Demand Forecast: Booking & Revenue</h1>", unsafe_allow_html=True)
    st.sidebar.header("MLOPS")
    choice1 =  st.sidebar.selectbox(" ",('Home','About Us'))
    choice2 =  st.sidebar.selectbox(" ",('Libraries used','SQLAlchemy','Psycopg2', 'Keras','Tensorflow','Boto3','Pandas','Streamlit'))
    choice3 =  st.sidebar.selectbox(" ",('Models implemented','Keras', 'ARIMA', 'DeepAR','Prophet','Amazon Forecast'))
    menu = ["AWS services used","Pipeline","Data Wrangler","Experiment and trial","Inference Job","End Points","Feature Store"]
    choice = st.sidebar.selectbox(" ",menu)
    st.sidebar.write('')
    st.sidebar.write('')
    href = f'<a style="color:black;" href="" class="button">Clear/Reset</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

    return choice1


