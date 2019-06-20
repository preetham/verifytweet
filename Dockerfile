FROM ubuntu:18.04
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
RUN apt-get update && apt-get install -y python3-dev python3-pip imagemagick tesseract-ocr libtesseract-dev
WORKDIR /app
COPY . .
RUN mkdir -p /data/files && \
    pip3 install virtualenv && \
    python3 -m virtualenv venv -p python3 && \
    . venv/bin/activate && \
    pip install -r requirements.txt
ENTRYPOINT ["/app/entrypoint.sh"]
