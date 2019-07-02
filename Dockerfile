FROM ubuntu:18.04
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt-get update &&  \
    apt-get install -y python3-dev python3-pip git \
    imagemagick tesseract-ocr libtesseract-dev
WORKDIR /app
COPY . .
RUN pip3 install pipenv && \
    python3 -m pipenv install
ENTRYPOINT ["/app/entrypoint.sh"]
