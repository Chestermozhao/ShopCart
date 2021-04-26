FROM python:3.8.8-buster

COPY . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/opt/app/entrypoint.sh"]

EXPOSE 8000
