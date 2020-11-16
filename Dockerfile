FROM python:3.8.6-alpine as base

WORKDIR /work
COPY /src/requirements.txt /work/requirements.txt

ENV PYTHONUNBUFFERED=1
RUN apk add build-base &&\
    apk add libressl-dev &&\
    apk add libffi-dev &&\
    apk add --update --no-cache python3 &&\
    ln -sf python3 /usr/bin/python
RUN python -m ensurepip
RUN pip install --no-cache --upgrade pip setuptools
RUN pip install -r /work/requirements.txt

COPY /src/ /work/

# run python code
CMD python /work/run.py run -h 0.0.0.0
