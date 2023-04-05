FROM python:3.9-slim-buster

WORKDIR /app

COPY ./app /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python","web-srv.py" ]

CMD [ "log" ]
