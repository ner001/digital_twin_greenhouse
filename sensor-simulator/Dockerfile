FROM python:3.10-slim
WORKDIR /app
COPY simulate_sensors.py .
RUN pip install kafka-python
CMD ["python", "simulate_sensors.py"]
