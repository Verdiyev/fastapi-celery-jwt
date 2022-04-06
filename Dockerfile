FROM python:3.10.0-slim
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install python3-dev default-libmysqlclient-dev build-essential libssl-dev
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app