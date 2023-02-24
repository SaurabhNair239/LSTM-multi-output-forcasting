import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import load_model
import datetime
import s3_op


def ready_data_for_lstm(data,step):
    x,y = [], []
    for i in range(len(data)-step-1):
        x.append(data[i:(i+step)])
        y.append(data[(i+step)])
    return np.array(x),np.array(y)

def amazon_prediction():
    real_data = pd.read_csv(s3_op.get_data_from_s3("final_data.csv"))
    data = real_data[real_data["company_id"]=="amzn"]
    data = data.drop(["Date","company_id"],axis=1)

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    test = data_scaled[int(round(len(data)*0.80,0)):]

    model = load_model("lstm_model.h5")
    fut_data = []
    for i in range(0,14):
        X_test,y_test = ready_data_for_lstm(test,14)
        temp_pred_data = model.predict(X_test)
        fut_data.append(temp_pred_data[-1].tolist())
        test = np.delete(test,0,axis=0)
        test = np.vstack((test,temp_pred_data[-1]))
    amazon_fut_prediction = pd.DataFrame(scaler.inverse_transform(fut_data),columns=["Open","High","Low","Close","Adj Close","Volume"])
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(20)]
    date_list = [x.date() for x in date_list if not x.isoweekday() in [6,7]]
    amazon_fut_prediction["Dates"] = date_list[:14]
    amazon_fut_prediction["company_id"] = "amzn"
    amazon_fut_prediction.to_csv("fut_data.csv",index=False,sep=',', encoding='utf-8')
