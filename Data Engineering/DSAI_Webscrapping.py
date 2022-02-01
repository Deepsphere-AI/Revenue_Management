########################################################

#Copyright (c) DeepSphere.AI 2021

# All rights reserved

# We are sharing this partial code for learning and research, and the idea behind us sharing the source code is to stimulate ideas #and thoughts for the learners to develop their MLOps.

# Author: # DeepSphere.AI | deepsphere.ai | dsschoolofai.com | info@deepsphere.ai

# Release: Initial release

#######################################################


import boto3
import json
from sqlalchemy import create_engine
import pandas as pd
import os
from google.cloud import secretmanager


class RedshiftConnection:
    
    username = None
    password = None
    engine = None
    host,port = None,None
    
    def __init__(self,username,passw,engine,host,port):
        self.username = username
        self.password = passw
        self.engine = engine
        self.host = host
        self.port = port
        self.connection = create_engine('postgresql://'+username+':'+passw+'@'+host+':'+str(port)+'/dev').connect()


    def write_redshift_booking(self,dataframe):
        val = dataframe.to_sql('flydubai_fact_transaction_booking_v3', self.connection, schema='ds_ai_fd_schema',index=False, if_exists ='append')
        self.connection.close()
        
    def write_redshift_revenue(self,dataframe):
        val = dataframe.to_sql('flydubai_fact_transaction_revenue_v3', self.connection, schema='ds_ai_fd_schema',index=False, if_exists ='append')
        self.connection.close()

    def read_redshift_data_booking(self):
        dataframe = pd.read_sql('''select data_category,data_source,model_name,travel_date,year,quarter,month,week,day,hour,region,origin,destination,flight,capacity,price_type,promotion,roundtrip_or_oneway,customer_type,product_type,location_lifestyle,location_economical_status,location_employment_status,location_event,source_precipitation,substring(source_wind,1,4) as source_wind,substring(destination_wind,1,4) as destination_wind,
substring(source_humidity,1,2) as source_humidity,substring(destination_humidity,1,2) as destination_humidity,destination_precipitation,number_of_booking,date,model_accuracy,accuracy_probability from ds_ai_fd_schema.flydubai_fact_transaction_booking_v3 where data_category='ACTUAL' ''',self.connection)
        return dataframe

    def read_redshift_data_revenue(self):
        dataframe = pd.read_sql('''select data_category,data_source,model_name,travel_date,year,quarter,month,week,day,hour,region,origin,destination,flight,capacity,price_type,promotion,roundtrip_or_oneway,customer_type,product_type,location_lifestyle,location_economical_status,location_employment_status,location_event,source_precipitation,substring(source_wind,1,4) as source_wind,substring(destination_wind,1,4) as destination_wind,
substring(source_humidity,1,2) as source_humidity,substring(destination_humidity,1,2) as destination_humidity,destination_precipitation,number_of_booking,currency,revenue,date,model_accuracy,accuracy_probability from ds_ai_fd_schema.flydubai_fact_transaction_revenue_v3 where data_category='ACTUAL' ''',self.connection)
        return dataframe
    
    def truncate_table_booking(self,model_name):
        dataframe = self.connection.execute('''delete ds_ai_fd_schema.flydubai_fact_transaction_booking_v3 where model_name = '''+"'"+model_name+"'")
        # self.connection.close()

    def truncate_table_revenue(self,model_name):
        dataframe = self.connection.execute('''delete ds_ai_fd_schema.flydubai_fact_transaction_revenue_v3 where model_name = '''+"'"+model_name+"'")
        # self.connection.close()


def get_gcp_secret():

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    
    # Build the resource name of the secret version.
    aws_access_key_name =  os.environ.get('GCP_SECRET_AWS_ACCESS_KEY','Specified environment variable GCP_SECRET_AWS_ACCESS_KEY is not set.')
    aws_secret_key_name =  os.environ.get('GCP_SECRET_AWS_SECRET_KEY','Specified environment variable GCP_SECRET_AWS_SECRET_KEY is not set.')
    
    # Access the secret version.
    aws_access_key_response = client.access_secret_version(request={"name": aws_access_key_name})
    aws_secret_key_response = client.access_secret_version(request={"name": aws_secret_key_name})
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    aws_access_key = aws_access_key_response.payload.data.decode("UTF-8")
    aws_secret_key = aws_secret_key_response.payload.data.decode("UTF-8")
    return aws_access_key,aws_secret_key

def get_aws_secret(aws_access_key,aws_secret_key):
    secret_name =  os.environ.get('AWS_SECRET_ARN','Specified environment variable AWS_SECRET_ARN is not set.')
    region_name = "us-east-2"
    secret = ''

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(secret)