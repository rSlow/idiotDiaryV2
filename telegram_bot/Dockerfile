FROM python:3.11

WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

# install chrome
RUN curl -LO  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
