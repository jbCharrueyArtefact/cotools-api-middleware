FROM python:3.9-slim

WORKDIR /code

RUN apt-get update && \
apt-get install --no-install-recommends -y vim git && \
rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]