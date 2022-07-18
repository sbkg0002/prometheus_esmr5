FROM python:3.9.13-slim-buster

# Inspired by:
# https://github.com/prometheus/client_python
# https://github.com/gejanssen/slimmemeter-rpi

RUN pip3 install --upgrade --no-cache \
        prometheus_client \
        smeterd

EXPOSE 8000

COPY  main.py /main.py
ENTRYPOINT ["/usr/local/bin/python3", "-u", "/main.py"]
