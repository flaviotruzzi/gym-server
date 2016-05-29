FROM ubuntu:latest

MAINTAINER Flavio Truzzi "flaviotruzzi@gmail.com"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev build-essential

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["gym_server.py"]
