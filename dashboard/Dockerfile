
FROM python:3.7

RUN apt-get update -y

ENV APP /banken

RUN mkdir $APP
WORKDIR $APP

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:8002", "app:app"]
