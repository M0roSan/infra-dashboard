
FROM python:3.6

RUN apt-get update -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app"]