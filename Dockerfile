FROM python:3.6-alpine

WORKDIR /srv/S2T/S2T_MainController

ADD . .

RUN apk add --update build-base
RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]


