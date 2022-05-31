# syntax=docker/dockerfile:1

FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y



WORKDIR /usr/src/SneakySnake

COPY requirements.txt .
COPY main.py .
COPY chessGame.py .
COPY chessImages chessImages
COPY rouletteImages rouletteImages
COPY quotes quotes

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]




