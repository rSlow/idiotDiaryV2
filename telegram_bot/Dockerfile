FROM python:3.11 as builder

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && apt-get -y dist-upgrade
RUN apt-get install -y google-chrome-stable

WORKDIR /app

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O ./chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
RUN unzip ./chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

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
