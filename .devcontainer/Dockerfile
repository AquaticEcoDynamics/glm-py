FROM jmad1v07/wet-glm

RUN apt update && apt install -y

# set environment variables
# from dockerising Django - https://github.com/testdrivenio/django-on-docker/blob/master/app/Dockerfile.prod
# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# prevent Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR /tmp
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir  

WORKDIR /tmp
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r requirements-dev.txt --no-cache-dir