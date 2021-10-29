FROM python:3.9

WORKDIR /code

RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y git

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ARG USER_EMAIL
ARG USER_NAME

RUN git config --global user.email ${USER_EMAIL}
RUN git config --global user.name ${USER_NAME}

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]