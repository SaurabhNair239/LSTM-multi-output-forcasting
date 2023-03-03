from api_data_daily import import_data_from_api
from s3_op import dump_file_to_s3 
from amazon_ts import amazon_prediction
    
import_data_from_api()

dump_file_to_s3("final_data.csv")

amazon_prediction()

dump_file_to_s3("fut_data.csv")
    
