FROM python:3.9

ADD ./src /app/build/src

WORKDIR /app/build

RUN apt-get update && pip install paho-mqtt
   
CMD python3 ./src/subscriber.py
