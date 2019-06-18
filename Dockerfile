FROM python:3.7.3-stretch
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev
WORKDIR /app
COPY . .
RUN mkdir -p /data/files && \
    pip install virtualenv && \
    virtualenv venv -p python3 && \
    . venv/bin/activate && \
    pip install -r requirements.txt
ENTRYPOINT ["/app/entrypoint.sh"]