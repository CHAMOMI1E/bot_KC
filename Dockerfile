FROM python:alpine

LABEL authors="chamomile"

# Устанавливаем зависимости
RUN apk update && apk add --no-cache bash build-base

# Создаем виртуальную среду и активируем ее
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Устанавливаем зависимости
WORKDIR /pythonProject
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# Копируем файлы и билд
COPY ./ ./
RUN chmod -R 777 ./

# Запускаем приложение
CMD ["python3", "manage.py"]