FROM python:3.7

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

RUN pytest test.py
CMD python main.py
