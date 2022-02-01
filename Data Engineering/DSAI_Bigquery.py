########################################################

#Copyright (c) DeepSphere.AI 2021

# All rights reserved

# We are sharing this partial code for learning and research, and the idea behind us sharing the source code is to stimulate ideas #and thoughts for the learners to develop their MLOps.

# Author: # DeepSphere.AI | deepsphere.ai | dsschoolofai.com | info@deepsphere.ai

# Release: Initial release

#######################################################


from google.cloud import bigquery
import google.cloud.bigquery.dbapi as bq



class BigqueryConnection:
    
    def __init__(self):
        self.bqclient = bigquery.Client()
        
    def read_booking_table(self):
        query_string = """
        select data_category,data_source,model_name,travel_date,year,quarter,month,week,day,hour,region,origin,destination,flight,capacity,price_type,promotion,roundtrip_or_oneway,customer_type,product_type,location_lifestyle,location_economical_status,location_employment_status,location_event,source_precipitation,substr(source_wind,1,4) as source_wind,substr(destination_wind,1,4) as destination_wind,
source_humidity,destination_humidity,destination_precipitation,number_of_booking,case when substr(cast("0"||travel_date as string),-2,2)="24" then 
PARSE_TIMESTAMP("%m%d%Y%H",replace(cast("0"||travel_date as string),substr(cast("0"||travel_date as string),-2,2),"00"))
else PARSE_TIMESTAMP("%m%d%Y%H","0"||travel_date)
end as date,model_accuracy,accuracy_probability from airline_data.fact_transaction_booking_v2 where data_category='ACTUAL'
        """

        dataframe = (
            self.bqclient.query(query_string)
            .result()
            .to_dataframe(
                # Optionally, explicitly request to use the BigQuery Storage API. As of
                # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
                # API is used by default.
                create_bqstorage_client=True,
            )
        )
        return dataframe

    def read_revenue_table(self):
        query_string = """
        select data_category,data_source,model_name,travel_date,year,quarter,month,week,day,hour,region,origin,destination,flight,capacity,price_type,promotion,roundtrip_or_oneway,customer_type,product_type,location_lifestyle,location_economical_status,location_employment_status,location_event,source_precipitation,substr(source_wind,1,4) as source_wind,substr(destination_wind,1,4) as destination_wind,
source_humidity,destination_humidity,destination_precipitation,number_of_booking,currency,revenue,case when substr(cast("0"||travel_date as string),-2,2)="24" then 
PARSE_TIMESTAMP("%m%d%Y%H",replace(cast("0"||travel_date as string),substr(cast("0"||travel_date as string),-2,2),"00"))
else PARSE_TIMESTAMP("%m%d%Y%H","0"||travel_date)
end as date,model_accuracy,accuracy_probability from airline_data.fact_transaction_revenue_v2 where data_category='ACTUAL'
        """

        dataframe = (
            self.bqclient.query(query_string)
            .result()
            .to_dataframe(
                # Optionally, explicitly request to use the BigQuery Storage API. As of
                # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
                # API is used by default.
                create_bqstorage_client=True,
            )
        )
        return dataframe

    def truncate_revenue_table(self,model_name):
        try:
            con = bq.connect()
            cursor = con.cursor()
            query = '''
        delete airline_data.fact_transaction_revenue_v2 where model_name = '''+"'"+model_name+"'"
            cursor.execute(query)
            con.commit()
            con.close()
        except Exception as e:
            str(e)

    def truncate_booking_table(self,model_name):

        try:
            con = bq.connect()
            cursor = con.cursor()
            query = '''
        delete airline_data.fact_transaction_booking_v2 where model_name = '''+"'"+model_name+"'"
            cursor.execute(query)
            con.commit()
            con.close()
        except Exception as e:
            str(e)

    def write_booking_table(self,dataframe):
        job_config = bigquery.LoadJobConfig()
        table_id = "airline_data.fact_transaction_booking_v2"
        job = self.bqclient.load_table_from_dataframe(
    dataframe, table_id, job_config=job_config
)  # Make an API request.
        job.result()  # Wait for the job to complete.

        table = self.bqclient.get_table(table_id)  # Make an API request.
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )

    def write_revenue_table(self,dataframe):
        job_config = bigquery.LoadJobConfig()
        table_id = "airline_data.fact_transaction_revenue_v2"
        job = self.bqclient.load_table_from_dataframe(
    dataframe, table_id, job_config=job_config
)  # Make an API request.
        job.result()  # Wait for the job to complete.

        table = self.bqclient.get_table(table_id)  # Make an API request.
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )