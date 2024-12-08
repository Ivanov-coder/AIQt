FROM python:3.10-slim

ADD . /aiqt

WORKDIR /aiqt

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]