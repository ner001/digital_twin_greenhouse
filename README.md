# 🌱 Digital Twin Greenhouse System

A comprehensive digital twin solution for real-time monitoring and control of a smart greenhouse environment. This system creates and manages a virtual replica of a physical greenhouse using Apache NiFi, Apache Kafka, and a Flask-based dashboard.

<!-- Insert your "Screenshot 2025-05-20 144640" image here -->

## 🧠 Context and Objectives

A Digital Twin is a digital replica of a physical environment. This project aims to create a digital twin of a connected greenhouse, enabling:

- Real-time monitoring of climate conditions
- Automatic anomaly detection
- Centralized and visual environment management
- Virtual testing of security scenarios (e.g., intrusion detection)

This system can be implemented in agricultural applications, home automation, or internal security systems.

## 🧾 JSON Data Model

The simulated sensors produce data in this JSON format:

```json
{
  "sensor_id": "living_room",
  "temperature": 22.45,
  "humidity": 55.2,
  "motion": false,
  "door": null,
  "armed": true,
  "night": false,
  "timestamp": 1716200000
}
```

### Field Descriptions:

| Field | Description |
|-------|-------------|
| sensor_id | Room or sensor identifier (e.g., garage, kitchen) |
| temperature | Ambient temperature (°C) |
| humidity | Humidity level (%) |
| motion | Motion detection status (true/false) |
| door | Door status (open/closed) - only for garage sensor |
| armed | Security system activation status |
| night | Indicates whether it's nighttime |
| timestamp | UNIX timestamp of the reading |

## ⚙️ System Architecture

```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Simulated    │───▶│  Apache NiFi  │───▶│   Dashboard   │
│  Sensors      │    │  (Pipeline)   │    │   Flask+Plotly│
└───────────────┘    └───────────────┘    └───────────────┘
                            │                    
                            ▼                    
                     ┌───────────────┐           
                     │ Apache Kafka  │           
                     │ (Message Bus) │           
                     └───────────────┘           
```

## 🚀 Installation and Launch

### 🔧 Prerequisites

- Docker & Docker Compose
- Git
- Internet connection

### 📦 Installation

```bash
git clone https://github.com/ner001/digital-twin-greenhouse.git
cd digital-twin-greenhouse
docker-compose up --build
```

### 🧭 Available Interfaces

- NiFi UI: http://localhost:8080/nifi
- Dashboard: http://localhost:5000

## 📁 Project Structure

```
digital-twin-greenhouse/
├── docker-compose.yml          # Multi-container deployment
├── dashboard/                  # Flask application
│   ├── app.py
│   ├── templates/index.html
├── nifi/
│   └── smart_home_flow.xml     # NiFi pipeline template
├── sensor-simulator/           # Simulated data generation
│   ├── simulate_sensors.py
│   └── Dockerfile
└── .env                        # Environment variable configuration
```

## 🐳 Docker Compose Explanation

The docker-compose.yml file defines the following services:

- Zookeeper and Kafka for message handling
- Apache NiFi for data processing
- Sensor Simulator to simulate physical sensors
- Flask Dashboard for data visualization

Each service is isolated and communicates via a dedicated Docker network.

## 🛠️ Initial Configuration

1. Launch containers with `docker-compose up --build`
2. Open the NiFi interface at http://localhost:8080/nifi
3. Import the `nifi/smart_home_flow.xml` file
4. Start all processor groups
5. Access the dashboard at http://localhost:5000

## 📊 Expected Results

- Real-time sensor visualization: temperature, humidity, motion, door status
- Automatic anomaly detection
- Storage and display of historical data
- Responsive interface accessible on smartphones

## 🧪 NiFi Flow Example

- Extract data from Kafka
- Parse JSON
- Validate schema
- Transform data
- Generate alerts if temperature or humidity anomalies detected
- Reinject into Kafka (output topic)

## 🔄 Customization

### Adding a new sensor type:
1. Modify `sensor-simulator/simulate_sensors.py`
2. Adapt the flow in NiFi
3. Add graphs in `dashboard/app.py` and `index.html`

## 🧩 Troubleshooting

| Problem | Solution |
|---------|----------|
| Kafka not working | Check Zookeeper, ports, and connectivity |
| NiFi not displaying data | Verify topics, logs, and processor configuration |
| Empty dashboard | Verify data flow in Kafka, restart Flask |

View logs:

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