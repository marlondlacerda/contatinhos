FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip

RUN apk add make

RUN apk add bash

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install -r requirements.txt

COPY . .

CMD ["make", "run"]
