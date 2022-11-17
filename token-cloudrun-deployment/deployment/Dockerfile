FROM python:2.7

WORKDIR /app
COPY sleep-tracker/token-cloudrun/src /app
RUN pip install -r requirements.txt
CMD python main.py