FROM python:3.7

WORKDIR /app
COPY etl-service/src /app
RUN pip install -r requirements.txt
CMD python main.py