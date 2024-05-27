FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /app/core
COPY . /app
RUN cd .. && pip install -r requirements.txt