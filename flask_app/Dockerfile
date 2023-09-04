FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY flask_app/ /app/flask_app
WORKDIR /app/flask_app

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
