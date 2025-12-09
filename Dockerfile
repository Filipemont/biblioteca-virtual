FROM python:3.11-bookworm

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV MINIO_URL minio:9000
ENV MAIL_SERVER smtp.gmail.com
ENV MAIL_PORT 587

# hadolint ignore=DL3008,DL3015
RUN apt-get update && \
    apt-get install -yqq --no-install-recommends nginx tzdata pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV TZ America/Fortaleza
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone \
  && dpkg-reconfigure -f noninteractive tzdata

COPY nginx.conf /etc/nginx/nginx.conf
COPY ./app/ /app/
COPY requirements.txt /requirements.txt

# hadolint ignore=DL3013, DL3042
RUN pip install --upgrade pip && \
    python3.11 -m pip install  --no-cache-dir -r /requirements.txt

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# hadolint ignore=DL3025
CMD gunicorn --bind 0.0.0.0:5006 app:app --daemon & nginx -g 'daemon off;'
