FROM python:3.11

WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
RUN apt-get install firefox

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
