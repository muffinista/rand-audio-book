# NOTE -- newer versions of python are throwing this error for me
# https://github.com/sebp/scikit-survival/issues/333
FROM python:3.12.2-bullseye

ARG DEBIAN_FRONTEND=noninteractive

RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb  --no-check-certificate && \
    dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb --no-check-certificate -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt update \
    && apt -y --fix-broken install \
    && apt -y dist-upgrade \
    && apt-get install -y ffmpeg


WORKDIR /usr/src/app

COPY requirements.txt ./
#RUN pip install --upgrade setuptools wheel 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
