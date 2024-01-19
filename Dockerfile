# NOTE -- newer versions of python are throwing this error for me
# https://github.com/sebp/scikit-survival/issues/333
FROM python:3.10-bullseye

#FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get update \
#     && apt-get install -y \
#     curl \
#     libc6 \
#     libgcc1 \
#     libgssapi-krb5-2 \
#     libicu66 \
#     libssl1.1 \
#     libstdc++6 \
#     zlib1g \
#     build-essential libssl-dev ca-certificates \
#     wget

#    libasound2  \
#    libgstreamer1.0-0 gstreamer1.0-plugins-base \
#    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
#    ffmpeg
#    libpthread-stubs0-dev \


# RUN wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf - 
# WORKDIR /openssl-1.1.1u
# RUN ./config --prefix=/usr/local \
#     && make -j $(nproc) \
#     && make install_sw install_ssldirs \
#     && ldconfig -v \
#     && export SSL_CERT_DIR=/etc/ssl/certs
# WORKDIR /
# RUN rm -rf /openssl-1.1.1u
# ENV SSL_CERT_DIR=/etc/ssl/certs

# RUN update-ca-certificates

RUN wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb --no-check-certificate -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb
	
#RUN apt-get update \
#	&& apt-get install -y dotnet-runtime-8.0 aspnetcore-runtime-8.0 \
#	&& rm -rf /var/lib/apt/lists/*

#RUN useradd -ms /bin/bash app
#USER app


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
