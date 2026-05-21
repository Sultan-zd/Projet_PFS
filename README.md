<div align="center">

# 🚗 Smart Parking Analysis

### Système Intelligent et Sécurisé de Gestion et d'Analyse des Parkings Urbains par Vision par Ordinateur

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6F00?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

---

*Projet de Fin de Semestre — Conception d'un système complet intégrant intelligence artificielle, backend sécurisé et interface web moderne pour la gestion intelligente des parkings.*

</div>

---

## 📋 Table des Matières

- [Présentation](#-présentation)
- [Architecture](#-architecture)
- [Technologies](#-technologies-utilisées)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation & Lancement](#-installation--lancement)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Structure du Projet](#-structure-du-projet)
- [Captures d'Écran](#-captures-décran)
- [Auteurs](#-auteurs)

---

## 🎯 Présentation

**Smart Parking Analysis** est un système complet de gestion et d'analyse de parkings urbains basé sur la **vision par ordinateur**. Le système utilise l'intelligence artificielle (YOLOv8) pour détecter en temps réel l'état d'occupation des places de parking à partir de flux vidéo ou d'images, puis transmet ces données à un backend sécurisé qui alimente un dashboard web interactif.

### Objectifs du Projet

| Objectif | Description |
|----------|-------------|
| 🧠 **Détection IA** | Détecter automatiquement les véhicules et classifier les places (occupée/libre) |
| 📊 **Analyse en temps réel** | Visualiser l'état du parking en direct avec rafraîchissement automatique |
| 📈 **Statistiques avancées** | Analyser les tendances d'occupation (heures de pointe, rotation, durée) |
| 🔒 **Sécurité** | Authentification JWT avec rôles (Admin/Visiteur) |
| 🌐 **Interface moderne** | Dashboard web professionnel avec design premium |

---

## 🏗 Architecture

Le système est composé de **3 modules interconnectés** :

```
┌─────────────────────┐     HTTP/REST     ┌──────────────────────┐     HTTP/REST     ┌─────────────────────┐
│                     │ ───────────────── │                      │ ───────────────── │                     │
│   🐍 Module IA      │    POST /update   │   ☕ Backend Java     │    GET /places    │   ⚛️  Frontend React │
│   Python + YOLOv8   │ ───────────────── │   Spring Boot + JWT  │ ───────────────── │   Dashboard Web     │
│                     │                   │                      │                   │                     │
│  • Détection vidéo  │                   │  • API REST          │                   │  • Temps réel       │
│  • FastAPI server   │                   │  • MySQL + JPA       │                   │  • Graphiques       │
│  • Anti-flickering  │                   │  • Spring Security   │                   │  • Historique       │
│                     │                   │  • Swagger UI        │                   │  • Responsive       │
└─────────────────────┘                   └──────────────────────┘                   └─────────────────────┘
     Port 8000                                 Port 8080                                  Port 5173
```

### Flux de Données

1. **Caméra / Vidéo** → Le module IA capture les images
2. **YOLOv8** → Analyse chaque frame et détecte les véhicules
3. **Python → Spring Boot** → Envoie l'état de chaque place via `POST /api/parking/update`
4. **Spring Boot → MySQL** → Persiste l'état et crée l'historique d'occupation
5. **React → Spring Boot** → Récupère les données via `GET /api/parking/places`
6. **Dashboard** → Affiche l'état en temps réel et les statistiques

---

## 🛠 Technologies Utilisées

### Module IA (Python)
| Technologie | Version | Rôle |
|-------------|---------|------|
| Python | 3.10+ | Langage principal |
| YOLOv8 (Ultralytics) | 8.x | Détection d'objets / Classification |
| OpenCV | 4.8+ | Traitement d'images et vidéos |
| FastAPI | 0.110+ | Microservice REST pour l'IA |
| NumPy | 1.24+ | Calculs matriciels |

### Backend (Java)
| Technologie | Version | Rôle |
|-------------|---------|------|
| Java | 17 | Langage principal |
| Spring Boot | 3.2.1 | Framework backend |
| Spring Security | 6.x | Sécurité et authentification |
| Spring Data JPA | 3.x | ORM / Accès base de données |
| MySQL | 8.0 | Base de données relationnelle |
| JWT (jjwt) | 0.11.5 | Tokens d'authentification |
| Springdoc OpenAPI | 2.3.0 | Documentation Swagger |

### Frontend (React)
| Technologie | Version | Rôle |
|-------------|---------|------|
| React | 19 | Framework UI |
| Vite | 8.x | Build tool |
| React Router | 6.x | Navigation SPA |
| Recharts | 2.x | Graphiques et visualisation |
| React Icons | 5.x | Icônes |
| Framer Motion | 11.x | Animations |
| Axios | 1.x | Client HTTP |

---

## ✨ Fonctionnalités

### 🧠 Module IA
- ✅ Détection autonome avec modèle entraîné (best.pt)
- ✅ Détection avec zones prédéfinies (places.json)
- ✅ Anti-flickering (temporisation 10s pour éviter les faux positifs)
- ✅ Serveur FastAPI pour upload et analyse d'images
- ✅ Outil interactif de configuration des places
- ✅ Script d'entraînement personnalisable
- ✅ Support vidéo, webcam, et photos

### ☕ Backend
- ✅ Architecture en couches (Controller → Service → Repository)
- ✅ Authentification JWT sécurisée
- ✅ Gestion automatique de l'historique d'occupation
- ✅ Endpoints de statistiques avancées (horaires, journaliers, rotation)
- ✅ Initialisation automatique des données (38 places, compte admin)
- ✅ Documentation Swagger UI
- ✅ CORS configuré

### ⚛️ Frontend
- ✅ Dashboard avec KPIs en temps réel
- ✅ Monitoring live avec grille de places animée
- ✅ Graphiques interactifs (Pie, Area, Bar charts)
- ✅ Page d'historique avec recherche et pagination
- ✅ Page de connexion premium avec split layout
- ✅ Navigation par sidebar avec icônes
- ✅ Design glassmorphism / dark mode
- ✅ Animations et transitions fluides
- ✅ Responsive design

---

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

| Outil | Version Minimum | Vérification |
|-------|----------------|--------------|
| **Python** | 3.10+ | `python --version` |
| **Java JDK** | 17+ | `java -version` |
| **Node.js** | 18+ | `node --version` |
| **MySQL** | 8.0+ | `mysql --version` |
| **Maven** | 3.8+ | `mvn --version` |
| **npm** | 9+ | `npm --version` |

---

## 🚀 Installation & Lancement

### 1️⃣ Base de Données MySQL

```sql
-- Créer la base de données
CREATE DATABASE smart_parking;
```

### 2️⃣ Module IA (Python)

```bash
# Naviguer vers le module IA
cd 1_IA_Python

# Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur FastAPI
python server.py
# → Serveur IA disponible sur http://localhost:8000
# → Documentation API sur http://localhost:8000/docs

# OU lancer un script de détection directement
python scripts/analyse_video_autonome.py
python scripts/analyse_video_zones.py
python scripts/analyse_photos.py
```

### 3️⃣ Backend Spring Boot

```bash
# Naviguer vers le backend
cd 2_Backend_Java/api

# Compiler et lancer
mvn clean install -DskipTests
mvn spring-boot:run
# → API disponible sur http://localhost:8080
# → Swagger UI sur http://localhost:8080/swagger-ui.html

# Compte admin créé automatiquement :
# 📧 Utilisateur : admin
# 🔑 Mot de passe : admin123
```

### 4️⃣ Frontend React

```bash
# Naviguer vers le frontend
cd 3_Frontend_React/frontend-parking

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
# → Interface disponible sur http://localhost:5173
```

### ▶️ Ordre de Lancement

```
1. MySQL           → La base doit être en cours d'exécution
2. Spring Boot     → Crée les tables et le compte admin
3. Python (IA)     → Commence à analyser et envoyer les données
4. React           → Affiche le dashboard en temps réel
```

---

## ⚙️ Configuration

### Base de Données

Fichier : `2_Backend_Java/api/src/main/resources/application.properties`

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/smart_parking
spring.datasource.username=root
spring.datasource.password=
```

### Module IA

Fichier : `1_IA_Python/config.py`

```python
# URL de l'API Spring Boot
SPRING_BOOT_API_URL = "http://localhost:8080/api/parking/update"

# Seuils de détection
CONFIDENCE_THRESHOLD = 0.25
ANTI_FLICKER_DELAY_SECONDS = 10

# Intervalle d'envoi des données
SEND_INTERVAL_SECONDS = 3.0
```

---

## 📖 API Documentation

### Endpoints Publics

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/auth/login` | Authentification (retourne un token JWT) |
| `GET` | `/api/parking/places` | Liste des places avec état actuel |
| `POST` | `/api/parking/update` | Mise à jour depuis le module IA |
| `GET` | `/api/parking/summary` | Résumé rapide (total, occupées, libres) |

### Endpoints Admin (JWT requis)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/stats/dashboard` | Résumé complet du dashboard |
| `GET` | `/api/stats/hourly` | Statistiques par heure |
| `GET` | `/api/stats/daily` | Statistiques par jour |
| `GET` | `/api/stats/rotation` | Taux de rotation par place |
| `GET` | `/api/stats/recent` | 20 dernières activités |
| `GET` | `/api/stats/history` | Historique complet |

### Endpoints FastAPI (Module IA)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/status` | État du serveur IA |
| `POST` | `/api/analyze` | Analyser une image uploadée |
| `POST` | `/api/analyze-batch` | Analyser un lot d'images |
| `GET` | `/api/zones` | Liste des zones configurées |

---

## 📁 Structure du Projet

```
Smart-Parking-Analysis/
│
├── 1_IA_Python/                    # Module Intelligence Artificielle
│   ├── config.py                   # Configuration centralisée
│   ├── server.py                   # Serveur FastAPI (microservice IA)
│   ├── requirements.txt            # Dépendances Python
│   ├── modeles/
│   │   ├── best.pt                 # Modèle entraîné (parking)
│   │   └── yolov8n.pt              # Modèle COCO pré-entraîné
│   ├── scripts/
│   │   ├── detection_engine.py     # Moteur de détection unifié
│   │   ├── analyse_video_autonome.py
│   │   ├── analyse_video_zones.py
│   │   ├── analyse_photos.py
│   │   ├── entrainer_ia.py
│   │   └── definir_places.py
│   └── medias/                     # Vidéos, images, places.json
│
├── 2_Backend_Java/                 # Backend REST API
│   └── api/
│       ├── pom.xml
│       └── src/main/java/com/smartparking/api/
│           ├── ApiApplication.java
│           ├── config/             # SecurityConfig
│           ├── model/              # PlaceParking, OccupationHistory, AppUser
│           ├── repository/         # JPA Repositories avec requêtes stats
│           ├── service/            # ParkingService, AuthService, StatisticsService
│           ├── controller/         # ParkingController, AuthController, StatisticsController
│           ├── dto/                # LoginRequest, LoginResponse, DashboardStatsResponse
│           ├── security/           # JwtUtil, JwtRequestFilter, UserDetailsServiceImpl
│           └── init/               # DataInitializer (admin + 38 places)
│
├── 3_Frontend_React/               # Interface Web
│   └── frontend-parking/
│       ├── package.json
│       └── src/
│           ├── App.jsx             # Routes principales
│           ├── main.jsx            # Point d'entrée
│           ├── index.css           # Design system
│           ├── api/axios.js        # Client HTTP configuré
│           ├── context/AuthContext.jsx
│           ├── components/
│           │   ├── layout/         # Sidebar, Header, Layout
│           │   ├── dashboard/      # StatCard
│           │   └── parking/        # ParkingSpot, ParkingGrid
│           └── pages/
│               ├── DashboardPage   # Vue d'ensemble + graphiques
│               ├── LiveMonitorPage # Monitoring temps réel
│               ├── AnalyticsPage   # Statistiques avancées
│               ├── HistoryPage     # Historique paginé
│               ├── LoginPage       # Connexion admin
│               └── SettingsPage    # Infos système
│
└── README.md                       # Ce fichier
```

---

## 🔐 Sécurité

- **Authentification JWT** : Token signé HMAC-SHA256, expire après 10 heures
- **BCrypt** : Mots de passe hashés avec BCrypt (jamais stockés en clair)
- **CORS** : Configuré pour n'autoriser que les origines frontend
- **Rôles** : `ROLE_ADMIN` pour l'accès aux statistiques et à l'historique
- **Stateless** : Pas de session côté serveur (architecture REST pure)

---

## 🤖 Modèles IA

### Modèle Autonome (`best.pt`)
- Entraîné sur un dataset personnalisé de parking
- Classes : `occupied` (occupée), `available` (libre)
- Classifie directement chaque place détectée

### Modèle COCO (`yolov8n.pt`)
- Modèle pré-entraîné sur le dataset COCO
- Détecte les véhicules (car, truck, bus)
- Utilisé avec les zones prédéfinies (places.json)

### Entraîner votre propre modèle

```bash
cd 1_IA_Python
python scripts/entrainer_ia.py 50   # 50 epochs
# Le modèle sera sauvegardé dans runs/
# Copiez best.pt dans modeles/ pour l'utiliser
```

---

## 📄 Licence

Ce projet est développé dans le cadre d'un **Projet de Fin de Semestre (PFS)**.

---

<div align="center">

**Développé avec ❤️ en utilisant Python, Java et React**

</div>
