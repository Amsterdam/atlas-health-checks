FROM python:3.7.0
LABEL maintainer="datapunt@amsterdam.nl"

WORKDIR /home
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY tests/ tests/
CMD pytest
