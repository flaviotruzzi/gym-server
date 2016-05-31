FROM ubuntu:latest

MAINTAINER Flavio Truzzi "flaviotruzzi@gmail.com"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev build-essential         \
                       xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi \
                       xfonts-scalable xfonts-cyrillic x11-apps      \
                       libjpeg-dev libpng12-dev python-opengl

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000 8000

ENV ON_DOCKER 1

ENTRYPOINT ["/bin/bash"]

CMD ["start.sh"]
