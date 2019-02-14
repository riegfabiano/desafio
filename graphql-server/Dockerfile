FROM python:3.4.9-alpine

WORKDIR /app

ADD ./app /app

COPY ./requirements.txt /etc

RUN pip install --no-cache-dir -r /etc/requirements.txt

EXPOSE 5000

ENV HOST_A desafio-sistema-a.westus.azurecontainer.io
ENV HOST_B desafio-sistema-b.westus.azurecontainer.io
ENV HOST_C desafio-sistema-c.westus.azurecontainer.io

CMD ["python", "app.py"]