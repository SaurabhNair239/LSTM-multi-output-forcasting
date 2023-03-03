FROM python:3.6.9

WORKDIR /app

COPY api_data_daily.py .

COPY s3_op.py .

COPY lstm_model.h5 .

COPY amazon_ts.py .

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

CMD worker: python app.py
