FROM python:3.6.9-stretch

RUN mkdir /app
COPY . /app

RUN python -m pip install -r /app/requirements.txt
RUN mkdir /app/data

WORKDIR /app

CMD [ "python3", "main.py" ]