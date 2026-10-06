FROM apache/airflow:3.3.2-python3.12
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt