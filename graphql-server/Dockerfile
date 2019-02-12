FROM python:3.4.9-alpine

WORKDIR /app

ADD ./app /app

COPY ./requirements.txt /etc

RUN pip install --no-cache-dir -r /etc/requirements.txt

EXPOSE 8080

ENV HOST_A localhost
ENV HOST_B localhost
ENV HOST_C localhost

CMD ["python", "app.py"]