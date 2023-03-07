FROM python:3.6.9-alpine

ARG aws_access_key_id
ARG aws_secret_access_key

RUN echo "$aws_access_key_id"
RUN echo "$aws_secret_access_key"

ENV aws_access_key_id_val  $aws_access_key_id
ENV aws_secret_access_key_val $aws_secret_access_key

RUN echo $aws_access_key_id_val
RUN echo $aws_secret_access_key_val

WORKDIR /app

COPY api_data_daily.py .

#COPY .github/workflows/main.yaml main.yaml

COPY set_env_var.py .

COPY s3_op.py .

COPY lstm_model.h5 .

COPY amazon_ts.py .

COPY app.py .

COPY requirements.txt .

RUN PYTHONPATH=/usr/bin/python pip install --upgrade pip

RUN PYTHONPATH=/usr/bin/python pip install -r requirements.txt
#RUN pip install -r /app/requirements.txt

# CMD ["python", "/app/app.py"]

CMD ["python", "/app/set_env_var.py"]


