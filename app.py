import /app/api_data_daily as adds
import /app/s3_op as s3
import /app/amazon_ts as ats
    
adds.import_data_from_api()

s3.dump_file_to_s3("final_data.csv")

ats.amazon_prediction()

s3.dump_file_to_s3("fut_data.csv")
    
