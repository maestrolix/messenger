FROM python:3.8-alpine

WORKDIR /usr/src/messenger

# Python не будет пытаться создавать файлы .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Гарантирует, что наш вывод консоли выглядит знакомым и не буферизируется Docker
ENV PYTHONUNBUFFERED 1

# Обновление пакетов
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

# Устанавливаем зависимости psycopg2
RUN apk add postgresql-dev gcc python3-dev musl-dev

# Установка пакетов
RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

# Копируем entrypoint.sh
COPY ./entrypoint.sh .

# Копируем проект
COPY . .

ENTRYPOINT ["/usr/src/messenger/entrypoint.sh"]