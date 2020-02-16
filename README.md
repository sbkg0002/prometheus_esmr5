# Prometheus exporter for ESMR 5.0
Smart Meter ESMR 5.0 Prometheus exporter

Currently for arm32v7 only.

To run in Docker:
```
docker run --detach --name prometheus_esmr5 --publish 8000:8000 --device=/dev/ttyUSB0 sbkg0002/prometheus_esmr5:arm32v7-latest
```

You can view the metrics at http://localhost:8000/metrics
