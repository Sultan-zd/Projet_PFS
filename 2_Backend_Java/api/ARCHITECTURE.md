# 🏛️ Architecture du Projet Smart Parking IA

Ce document détaille la structure et le rôle de chaque fichier et composant majeur du projet. L'architecture est divisée en trois blocs principaux : le **Backend** (API Java Spring Boot), le **Frontend** (React), et l'**Intelligence Artificielle** (Python).

## 🌊 Vue d'ensemble du Flux de Données

Le système fonctionne de la manière suivante :

1.  **L'IA (Python)** analyse un flux vidéo ou des images.
2.  Elle détecte l'état de chaque place de parking (libre/occupée).
3.  Lorsqu'un changement d'état est détecté, l'IA envoie une requête HTTP POST au **Backend (Java)**.
4.  Le **Backend** reçoit la requête, met à jour l'état de la place dans la base de données **MySQL**, et enregistre un historique.
5.  Le **Frontend (React)** interroge périodiquement le **Backend** pour obtenir l'état à jour de toutes les places et les affiche à l'utilisateur.
6.  Un administrateur peut se connecter via le **Frontend**, qui obtient un **Token JWT** du **Backend** pour accéder à des routes protégées (comme l'historique).

---

## ☕ Backend (API Java Spring Boot)

Le backend est le cerveau central qui gère les données, la logique métier et la sécurité.

### Fichiers de Configuration

-   **`pom.xml`**
    -   **Rôle** : Fichier de configuration de Maven. Il définit toutes les dépendances externes du projet (Spring Boot, Spring Data JPA, Spring Security, JWT, driver MySQL, etc.) et comment compiler le projet.

-   **`src/main/resources/application.properties`**
    -   **Rôle** : Fichier de configuration principal de Spring Boot.
    -   **Contenu** : Contient les informations critiques pour que l'application fonctionne, notamment :
        -   L'URL de connexion à la base de données MySQL (`spring.datasource.url`).
        -   Les identifiants (`username`, `password`).
        -   La configuration d'Hibernate pour la gestion de la base de données (`spring.jpa.hibernate.ddl-auto=update`).

### Modèles de Données (Entités JPA)

Ces classes représentent les tables dans la base de données.

-   **`AppUser.java`**
    -   **Rôle** : Représente un utilisateur (ex: admin) dans la table `users`. Contient son nom d'utilisateur, son mot de passe haché et son rôle (`ROLE_ADMIN`).

-   **`PlaceParking.java`**
    -   **Rôle** : Représente une place de parking dans la table `places_parking`. Contient son numéro, son état (`occupee`), et la date/heure du début d'occupation.

-   **`OccupationHistory.java`**
    -   **Rôle** : Représente une entrée dans la table d'historique. Chaque fois qu'une place change d'état, une nouvelle ligne est créée ici pour la traçabilité.

### Couche d'Accès aux Données (Repositories)

Ces interfaces permettent de communiquer avec la base de données sans écrire de SQL.

-   **`AppUserRepository.java`**, **`PlaceParkingRepository.java`**, **`OccupationHistoryRepository.java`**
    -   **Rôle** : Interfaces Spring Data JPA qui fournissent automatiquement les méthodes pour les opérations CRUD (Create, Read, Update, Delete) sur les entités correspondantes. On peut y ajouter des méthodes personnalisées comme `findByUsername(String username)`.

### Couche de Sécurité (Spring Security & JWT)

-   **`SecurityConfig.java`**
    -   **Rôle** : Fichier central de la configuration de sécurité. Il définit :
        -   Quelles URLs sont publiques (`/api/auth/login`, `/api/parking/places`) et lesquelles nécessitent une authentification.
        -   La configuration **CORS** pour autoriser le Frontend React à communiquer avec l'API.
        -   La politique de session (`STATELESS`) car nous utilisons des tokens JWT et non des sessions.
        -   Le `PasswordEncoder` (BCrypt) pour hacher les mots de passe.

-   **`JwtUtil.java`**
    -   **Rôle** : Classe utilitaire pour gérer les JSON Web Tokens (JWT). Ses responsabilités sont de **générer** un token après une connexion réussie et de **valider** un token reçu dans une requête.

-   **`JwtRequestFilter.java`**
    -   **Rôle** : Un filtre qui s'exécute sur **chaque requête** entrante. Il intercepte la requête, cherche un token JWT dans l'en-tête `Authorization`, le valide, et si le token est correct, il configure le contexte de sécurité de Spring pour autoriser la requête.

### Couche API (Controllers)

Ces classes exposent les points d'entrée (endpoints) de l'API REST.

-   **`AuthController.java`**
    -   **Rôle** : Gère le processus d'authentification.
    -   **Endpoint** : `/api/auth/login`. Reçoit un nom d'utilisateur et un mot de passe, les vérifie, et si c'est correct, renvoie un token JWT.

-   **`ParkingController.java`**
    -   **Rôle** : Gère toutes les opérations liées au parking.
    -   **Endpoints** :
        -   `/api/parking/places` : (GET) Utilisé par le Frontend React pour obtenir l'état de toutes les places.
        -   `/api/parking/update` : (POST) Utilisé par le script Python pour mettre à jour l'état d'une place.
        -   `/api/parking/historique` : (GET) Route protégée pour que les admins puissent voir l'historique.

### Autres

-   **`DataInitializer.java`**
    -   **Rôle** : Une classe qui s'exécute au démarrage de l'application. Elle vérifie si la base de données est vide et, si c'est le cas, crée un compte administrateur par défaut.

---

## 🧠 Intelligence Artificielle (Python)

Cette partie est responsable de la vision par ordinateur.

### `outils/analyse_avec_places/` (Méthode Géométrique)

-   **`definir_places.py`**
    -   **Rôle** : Script utilitaire exécuté une seule fois. Il permet à l'utilisateur de dessiner des polygones sur une image du parking pour définir les zones de chaque place.

-   **`places.json`**
    -   **Rôle** : Fichier de configuration généré par le script ci-dessus. Il contient les coordonnées de tous les polygones dessinés, servant de "carte" du parking.

-   **`analyse_video.py`**
    -   **Rôle** : Script principal d'analyse. Il charge la vidéo, utilise le modèle YOLOv8 de base pour détecter les "voitures", puis vérifie si le centre de chaque voiture détectée se trouve à l'intérieur d'un des polygones définis dans `places.json`. Si l'état d'une place change, il envoie une mise à jour au backend.

### `outils/analyse_autonome/` (Méthode Autonome)

-   **`best.pt`**
    -   **Rôle** : C'est le cerveau de cette méthode. Il s'agit d'un modèle YOLOv8 qui a été **surentraîné** non pas pour voir des "voitures", mais pour reconnaître directement les classes "libre" et "occupée".

-   **`analyse_live.py`** / **`analyse_photos.py`**
    -   **Rôle** : Scripts d'analyse qui utilisent le modèle `best.pt`. Leur logique est plus simple : ils exécutent le modèle sur une image/frame, et le modèle leur dit directement si la place est "libre" ou "occupée", sans avoir besoin de configuration géométrique.

---

## 💻 Frontend (React)

Le frontend est l'interface utilisateur visible dans le navigateur. Bien que les fichiers ne soient pas listés ici, son rôle est de :

1.  **Afficher le Parking** : Envoyer une requête GET à `/api/parking/places` pour récupérer l'état de toutes les places et les afficher visuellement.
2.  **Gérer la Connexion** : Fournir un formulaire de connexion qui envoie une requête POST à `/api/auth/login`.
3.  **Stocker le Token** : Une fois le token JWT reçu, le stocker de manière sécurisée (ex: `localStorage`).
4.  **Envoyer des Requêtes Authentifiées** : Pour les actions réservées aux admins, inclure le token JWT dans l'en-tête `Authorization` de la requête.
