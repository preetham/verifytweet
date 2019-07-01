FROM circleci/python:3.7.3
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
RUN apt-get update && apt-get install -y git \
    imagemagick tesseract-ocr libtesseract-dev
WORKDIR /app
COPY . .
ENTRYPOINT ["/app/entrypoint.sh"]
