FROM python:3.10[p

LABEL authors="chamomile"


WORKDIR /bot_KC



COPY ./requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./ ./



RUN chmod -R 777 ./

