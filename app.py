import api_data_daily
import s3_op
import amazon_ts
from flask import Flask,render_template,request
#get data from API and store it into repo


app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():

    api_data_daily.import_data_from_api()

    #upload the data from local system to S3 bucket
    s3_op.dump_file_to_s3("final_data.csv")

    #run lstm model
    amazon_ts.amazon_prediction()

    #push all prediction file to S3

    s3_op.dump_file_to_s3("fut_data.csv")

if __name__ == '__main__':
    app.run(debug=True)
