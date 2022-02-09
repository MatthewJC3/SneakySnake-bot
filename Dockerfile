# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /usr/src/SneakySnake

COPY requirements.txt .
COPY main.py .
COPY chessGame.py .
COPY chessImages .

RUN pip3 install -r requirements.txt

CMD ["python", "./main.py"]




