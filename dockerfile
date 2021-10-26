FROM python:3.9

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

WORKDIR /code

RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y git


COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app



# Downloading gcloud package
ENV HTTP_PROXY="http://fpc.itn.intraorange:8080"
ENV HTTPS_PROXY="http://fpc.itn.intraorange:8080" 

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]