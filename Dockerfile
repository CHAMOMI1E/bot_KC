FROM python:3.10

LABEL authors="chamomile"


# Устанавливаем зависимости
WORKDIR bot_KC/ .

COPY ./requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы и билд
COPY ./ ./
RUN chmod -R 777 ./

