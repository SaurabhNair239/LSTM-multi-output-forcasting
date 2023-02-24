FROM python:3.6.9

WORKDIR /app

COPY api_data_daily.py .

COPY s3_op.py .

COPY lstm_model.h5 .

COPY amazon_ts.py .

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

RUN chmod 0664 /etc/sron.d/crontab

RUN crontab /etc/cron.d/crontab

EXPOSE $PORT

CMD worker python app.py
