FROM python:3.9

ADD . /app/build/src

WORKDIR /app/build

RUN apt-get update && pip install paho-mqtt && pip install Flask

EXPOSE 5000
   
CMD python3 ./src/server.py
