FROM python:3.6.6-stretch

RUN mkdir /code
WORKDIR /code
ADD requeriments.txt /code/
RUN pip install -r requeriments.txt
ADD . /code/