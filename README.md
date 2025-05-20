# Digital Twin Greenhouse System
🌱 Digital Twin Greenhouse System
A comprehensive digital twin solution for real-time monitoring and control of a smart greenhouse environment. This system simulates and manages a virtual twin of a physical environment using Apache NiFi, Apache Kafka, and a Flask-based dashboard.

![Screenshot 2025-05-20 144640](https://github.com/user-attachments/assets/6ed68e53-bc7b-4bbd-afe8-a27d6dfcf01f)

🧠 Contexte et Objectif
Un Digital Twin est une réplique numérique d’un environnement réel. Ce projet vise à créer un jumeau numérique de serre connectée, permettant :

Une surveillance en temps réel des conditions climatiques

Une détection automatique des anomalies

Une gestion centralisée et visuelle de l’environnement

Un test virtuel de scénarios de sécurité (ex. intrusion)

Ce système peut être utilisé dans des applications agricoles, domotiques ou de sécurité intérieure.

🧾 Modèle de Données JSON
Les capteurs simulés produisent les données sous cette forme JSON :

json
Copier
Modifier
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
Description des Champs :
Champ	Description
sensor_id	Identifiant de la pièce ou du capteur (ex : garage, kitchen...)
temperature	Température ambiante (°C)
humidity	Taux d’humidité (%)
motion	Détection de mouvement (true/false)
door	Statut de la porte (ouverte/fermée) - uniquement pour le garage
armed	Système de sécurité activé ou non
night	Indique si c’est la nuit
timestamp	Horodatage UNIX du relevé

⚙️ Architecture du Système
scss
Copier
Modifier
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Capteurs     │───▶│  Apache NiFi  │───▶│   Dashboard   │
│  Simulés      │    │  (Pipeline)   │    │   Flask+Plotly│
└───────────────┘    └───────────────┘    └───────────────┘
                            │                    
                            ▼                    
                     ┌───────────────┐           
                     │ Apache Kafka  │           
                     │ (Message Bus) │           
                     └───────────────┘           
🚀 Installation et Lancement
🔧 Prérequis
Docker & Docker Compose

Git

Connexion Internet

📦 Installation
bash
Copier
Modifier
git clone https://github.com/ner001/digital-twin-greenhouse.git
cd digital-twin-greenhouse
docker-compose up --build
🧭 Interfaces disponibles
NiFi UI : http://localhost:8080/nifi

Dashboard : http://localhost:5000

📁 Structure du projet
bash
Copier
Modifier
digital-twin-greenhouse/
├── docker-compose.yml          # Lancement multi-conteneurs
├── dashboard/                  # Application Flask
│   ├── app.py
│   ├── templates/index.html
├── nifi/
│   └── smart_home_flow.xml     # Template de pipeline NiFi
├── sensor-simulator/           # Génération de données simulées
│   ├── simulate_sensors.py
│   └── Dockerfile
└── .env                        # Configuration des variables d'environnement
🐳 Explication du docker-compose.yml
Le fichier docker-compose.yml définit les services suivants :

Zookeeper et Kafka pour la gestion des messages

Apache NiFi pour le traitement des données

Sensor Simulator pour simuler les capteurs physiques

Dashboard Flask pour la visualisation des données

Chaque service est isolé et communique via un réseau Docker dédié.

🛠️ Configuration Initiale
Lancer les conteneurs avec docker-compose up --build

Ouvrir l’interface NiFi sur http://localhost:8080/nifi

Importer le fichier nifi/smart_home_flow.xml

Démarrer tous les groupes de processeurs

Accéder au dashboard sur http://localhost:5000

📊 Résultats Attendus
Visualisation temps réel des capteurs : température, humidité, mouvement, état de la porte

Détection automatique des anomalies

Stockage et affichage des données historiques

Interface responsive accessible sur smartphone


🧪 Exemple de Flux NiFi
Extraction de Kafka

Parsing JSON

Validation de schéma

Transformation de données

Génération d'alerte si température ou humidité anormale

Réinjection dans Kafka (output topic)

🔄 Personnalisation
Ajouter un nouveau type de capteur :
Modifier sensor-simulator/simulate_sensors.py

Adapter le flux dans NiFi

Ajouter les graphiques dans dashboard/app.py et index.html

🧩 Dépannage
Problème	Solution
Kafka ne fonctionne pas	Vérifier Zookeeper, ports et connectivité
NiFi n’affiche pas de données	Vérifier les topics, logs et configuration des processeurs
Dashboard vide	Vérifier que les données circulent dans Kafka, relancer Flask

Voir les logs :

bash
Copier
Modifier
docker-compose logs -f [service-name]
📜 Licence
Projet sous licence MIT. Voir le fichier LICENSE pour plus de détails.

🙏 Remerciements
Aux communautés Apache Kafka et NiFi

À Flask et Plotly pour les outils de visualisation

À tous les contributeurs et testeurs
