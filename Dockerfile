FROM tensorflow/tensorflow:latest-gpu-py3
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN pip install -r requirements.txt

COPY . /code/