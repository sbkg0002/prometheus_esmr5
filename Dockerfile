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
        prometheus_client \
        serial

# USER 3134
COPY  prometheus_esmr5 /prometheus_esmr5
WORKDIR /prometheus_esmr5
EXPOSE 8000/tcp
EXPOSE 8000/udp
CMD ["/usr/local/bin/python3", "/prometheus_esmr5/main.py"]