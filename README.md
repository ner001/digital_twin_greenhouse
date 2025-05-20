# Digital Twin Greenhouse System

A comprehensive digital twin solution for real-time greenhouse monitoring and control using Apache NiFi, Apache Kafka, and Flask.
![Screenshot 2025-05-20 144640](https://github.com/user-attachments/assets/6ed68e53-bc7b-4bbd-afe8-a27d6dfcf01f)

## Overview

This system creates a virtual representation of a greenhouse environment, enabling real-time monitoring and data analysis. By leveraging Apache NiFi for data processing, Apache Kafka for messaging, and a Flask-based dashboard, this project provides a complete solution for smart greenhouse management.

## Features

- **Real-time Environmental Monitoring**
  - Temperature, humidity, and light level sensors
  - Configurable sampling rates
  - Anomaly detection for sensor readings

- **Data Processing Pipeline**
  - Scalable data ingestion with Apache NiFi
  - Real-time data transformation and validation
  - Automated alert generation for out-of-range conditions

- **Message Streaming Architecture**
  - Event-driven design with Apache Kafka
  - Multi-topic organization for different data streams
  - Reliable message delivery

- **Interactive Dashboard**
  - Real-time visualization of all sensor metrics
  - Historical data trends
  - Mobile-responsive design for monitoring on any device

## System Architecture

```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│               │    │               │    │               │
│    Sensor     │───▶│  Apache NiFi  │───▶│   Dashboard   │
│   Simulator   │    │  Data Pipeline│    │               │
│               │    │               │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
                            │                    
                            │                    
                            ▼                    
                     ┌───────────────┐           
                     │               │           
                     │ Apache Kafka  │           
                     │  Message Bus  │           
                     │               │           
                     └───────────────┘           
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- Internet connection (for initial container downloads)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/digital-twin-greenhouse.git
   cd digital-twin-greenhouse
   ```

2. **Build and start the stack:**
   ```bash
   docker-compose up --build
   ```

3. **Access components:**
   - NiFi Interface: [http://localhost:8080/nifi](http://localhost:8080/nifi)
   - Dashboard: [http://localhost:5000](http://localhost:5000)

### Initial Configuration

1. **Import NiFi Template:**
   - Open NiFi UI at [http://localhost:8080/nifi](http://localhost:8080/nifi)
   - Upload and import `nifi/smart_home_flow.xml` template
   - Start all processor groups

## Component Details

### Sensor Simulator

Located in `sensor-simulator/` directory, this component:
- Generates realistic environmental data based on configurable parameters
- Simulates temperature, humidity, and light level variations
- Publishes data to Kafka topics at configurable intervals
- Easily customizable for different simulation scenarios

### Apache NiFi Data Pipeline

The NiFi flow (`nifi/smart_home_flow.xml`) implements:
- Data ingestion from Kafka topics
- JSON parsing and validation
- Alert generation for out-of-range conditions
- Data transformation and enrichment
- Publishing to downstream Kafka topics

### Dashboard Application

Built with Flask, Plotly, and Bootstrap for:
- Real-time visualization with automatically updating charts
- Historical data analysis with filtering capabilities
- Alert monitoring and management
- System health metrics
- Mobile-responsive design

## Advanced Configuration

### Environment Variables

The system can be configured via environment variables in the `.env` file:

```
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_REPLICATION_FACTOR=1

# NiFi Configuration
NIFI_WEB_HTTPS_PORT=8443

# Database Configuration
INFLUXDB_BUCKET=greenhouse
INFLUXDB_ORG=greenhouse-org
INFLUXDB_RETENTION=30d

# Simulator Configuration
SIMULATOR_INTERVAL_MS=5000
SIMULATOR_ANOMALY_PROBABILITY=0.01

# Dashboard Configuration
DASHBOARD_REFRESH_INTERVAL_MS=2000
```

### Production Deployment

For production environments:

1. Enable security features:
   - Uncomment security configurations in `docker-compose.yml`
   - Generate SSL certificates using the provided script
   - Configure authentication for NiFi, Kafka, and the dashboard

2. Scale components as needed:
   - Adjust service replicas in `docker-compose.yml`
   - Configure Kafka partitioning for higher throughput
   - Enable NiFi clustering for fault tolerance

## Development

### Project Structure

```
digital-twin-greenhouse/
├── docker-compose.yml
├── README.md
├── dashboard/
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── nifi/
│   └── smart_home_flow.xml
└── sensor-simulator/
    ├── Dockerfile
    ├── simulate_sensors.py
    └── docker-compose.yml
```

### Adding New Features

- **New Sensor Type:**
  1. Add sensor generation logic to `sensor-simulator/simulate_sensors.py`
  2. Update NiFi flow to process the new sensor data
  3. Add visualization components to the dashboard

- **Custom Visualization:**
  1. Modify `dashboard/templates/index.html` to add new chart elements
  2. Update `dashboard/app.py` to process and serve the new data
  3. Test with simulated sensor data

## Troubleshooting

### Common Issues

- **Kafka Connection Issues:**
  - Ensure Zookeeper is running and healthy
  - Check network connectivity between containers
  - Verify topic configurations

- **NiFi Flow Not Processing:**
  - Check processor configurations
  - Verify Kafka connection properties
  - Examine NiFi logs for errors

- **Dashboard Not Displaying Data:**
  - Confirm data is flowing through Kafka topics
  - Check browser console for JavaScript errors

### Logs

Access component logs:
```bash
docker-compose logs -f [service-name]
```

Available services:
- `zookeeper`
- `kafka`
- `nifi`
- `sensor-simulator`
- `dashboard`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Apache NiFi and Kafka communities
- Flask and Plotly for visualization components
- All contributors and testers
