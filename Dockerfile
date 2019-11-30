FROM arm32v7/python:3.8-slim-buster

# Inspired by:
# https://github.com/prometheus/client_python
# https://github.com/gejanssen/slimmemeter-rpi

RUN apt-get update && \
    apt-get upgrade -fy && \
    apt-get install -fy \
        python3-serial \
        cu &&\
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    pip3 install --upgrade --no-cache \
        prometheus_client 
        