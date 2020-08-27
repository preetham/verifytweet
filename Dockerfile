FROM python:3.7-slim-buster
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV VERIFYTWEET_RUN_FOR_WEB=true
RUN apt-get update &&  \
    apt-get install -y git build-essential \
    libblas-dev liblapack-dev libatlas-base-dev gfortran  \
    imagemagick tesseract-ocr libtesseract-dev libffi-dev
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["/app/entrypoint.sh"]
