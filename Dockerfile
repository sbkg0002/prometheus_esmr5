FROM python:3.9-slim-buster

# Inspired by:
# https://github.com/prometheus/client_python
# https://github.com/gejanssen/slimmemeter-rpi

RUN pip3 install --upgrade --no-cache \
        prometheus_client \
        smeterd

# USER 3134
WORKDIR /prometheus_esmr5
EXPOSE 8000/tcp
EXPOSE 8000/udp
COPY  prometheus_esmr5 /prometheus_esmr5
CMD ["/usr/local/bin/python3", "-u", "/prometheus_esmr5/main.py"]
