FROM python:3.9

ADD . /app/build/src

WORKDIR /app/build

RUN apt-get update && pip install kafka-python
   
CMD python3 ./src/consumer.py
