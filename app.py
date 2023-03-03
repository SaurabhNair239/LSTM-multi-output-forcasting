import api_data_daily
import s3_op
import amazon_ts
    
api_data_daily.import_data_from_api()

s3_op.dump_file_to_s3("final_data.csv")

amazon_ts.amazon_prediction()

s3_op.dump_file_to_s3("fut_data.csv")
    
