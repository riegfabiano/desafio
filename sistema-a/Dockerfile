FROM python:3.4.9-alpine

WORKDIR /app

ADD ./app /app

COPY ./requirements.txt /etc

RUN pip install --no-cache-dir -r /etc/requirements.txt

EXPOSE 5001

#ENV NAME World

CMD ["python", "app.py"]