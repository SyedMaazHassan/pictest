
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./code/* /code/
COPY ./code/docker-entrypoint.sh /code/
ENTRYPOINT ["/code/docker-entrypoint.sh"]
