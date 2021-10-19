FROM python:3.9.7-slim-buster

LABEL MAINTAINER="ivanovskyortega@outlook.com"

WORKDIR /technical-test/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT [ "python" , "main.py" ]