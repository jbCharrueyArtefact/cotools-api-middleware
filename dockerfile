FROM registry.gitlab.si.francetelecom.fr/lrousselotdesaintceran/co-tools-api-middleware/base

WORKDIR /code

COPY ./app /code/app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
