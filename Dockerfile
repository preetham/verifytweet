FROM ubuntu:18.04
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt-get update &&  \
    apt-get install -y python3-dev python3-pip \
    imagemagick tesseract-ocr libtesseract-dev
WORKDIR /app
COPY . .
RUN pip3 install pipenv && \
    python3 -m pipenv install
RUN groupadd --gid 3434 circleci \
    && useradd --uid 3434 --gid circleci --shell /bin/bash --create-home circleci \
    && echo 'circleci ALL=NOPASSWD: ALL' >> /etc/sudoers.d/50-circleci \
    && echo 'Defaults    env_keep += "DEBIAN_FRONTEND"' >> /etc/sudoers.d/env_keep
USER circleci
ENTRYPOINT ["/app/entrypoint.sh"]
