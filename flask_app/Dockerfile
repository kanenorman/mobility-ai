FROM python:3.10

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY flask_app/ /app/flask_app
WORKDIR /app/flask_app

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
