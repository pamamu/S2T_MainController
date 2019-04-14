FROM python:3.6-alpine

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG CONTAINER_LIST_PATH
ENV CONTAINER_LIST_PATH = $CONTAINER_LIST_PATH

WORKDIR /srv/S2T/S2T_MainController

ADD . .

RUN apk add --update build-base linux-headers
RUN pip install -r requirements.txt

CMD python src/app.py $SHARED_FOLDER $CONTAINER_LIST_PATH


