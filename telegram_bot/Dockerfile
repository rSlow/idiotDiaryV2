FROM python:3.11 as builder

ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.29.0
ENV FIREFOX_VER 87.0

WORKDIR /app

RUN set -x \
   && apt-get update \
   && apt-get upgrade -y \
   && apt-get install -y firefox-esr


# Add latest FireFox
RUN set -x \
   && apt-get install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/

# copy any python requirements file into the install directory and install all python requirements.
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# copy the source code into /app and move into that directory.
COPY . .

## start base stage.
# this is the image this is run.
FROM builder

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
