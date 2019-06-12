FROM centos:latest
LABEL author "Preetham Kamidi <kamidipreetham@gmail.com>"
ENV PYTHON_VERSION=3.6 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off
RUN yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/ && \
    rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/public_key  && \
    INSTALL_PKGS="rh-python36 rh-python36-python-devel rh-python36-python-setuptools \
    rh-python36-python-pip tesseract tesseract-langpack-deu ImageMagick ImageMagick-devel" && \
    yum update -y && \
    yum groupinstall 'Development Tools' -y && \
    yum install -y centos-release-scl && \
    yum -y --setopt=tsflags=nodocs install --enablerepo=centosplus $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum -y clean all --enablerepo='*'
WORKDIR /app
COPY . .
RUN source scl_source enable rh-python36 && \
    mkdir -p /data/files && \
    virtualenv venv -p python3 && \
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
ENTRYPOINT [ "entrypoint.sh" ]