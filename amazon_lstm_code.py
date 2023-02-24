import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
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

    train = data_scaled[:int(round(len(data)*0.80,0))]
    test = data_scaled[int(round(len(data)*0.80,0)):]

    X_train,y_train = ready_data_for_lstm(train,15)
    X_test,y_test = ready_data_for_lstm(test,15)

    model = Sequential()
    model.add(LSTM(128,return_sequences=True,input_shape = (X_train.shape[1],6)))
    model.add(LSTM(64,return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(6,activation="linear"))
    model.summary()

    model.compile(optimizer="adam",loss=["MSE"])
    model_history = model.fit(X_train,y_train,validation_data=(X_test,y_test),batch_size=15,epochs=15)

    model.save("lstm_model.h5")
    model_history_data = pd.DataFrame({"loss":model_history.history["loss"],
                                       "val_loss":model_history.history["val_loss"]})
    model_history_data.to_csv("model_history.csv")

    model = load_model("lstm_model.h5")
    X_train_pred = scaler.inverse_transform(model.predict(X_train))
    #X_train_pred_data = pd.DataFrame(X_train_pred)
    X_test_pred = model.predict(X_test)
    print(X_train_pred,X_test_pred)
