FROM python:3.11 as builder

WORKDIR /app

#download and install chrome
RUN apt-get -y update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# copy any python requirements file into the install directory and install all python requirements.
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# copy the source code into /app and move into that directory.
COPY . .

FROM builder

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
