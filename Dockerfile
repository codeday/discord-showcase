FROM python:3.7-slim-buster

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src /app/src/
WORKDIR /app
CMD ["python3", "src/main.py"]