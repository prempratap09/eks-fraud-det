FROM python:3.8.3-slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements.txt model.pkl /app/

RUN python -m pip install --upgrade pip \
    pip install -r requirements.txt

COPY app.py file_utils.py s3_utils.py /app/

CMD ["python", "app.py"]
