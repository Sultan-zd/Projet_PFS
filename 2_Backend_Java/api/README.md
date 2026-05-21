# 🚗 Projet Smart Parking IA - Full Stack

Bienvenue dans le guide d'installation complet du projet Smart Parking IA. Ce système combine la vision par ordinateur (IA), un backend robuste en Java Spring Boot sécurisé avec JWT, et une interface frontend dynamique en React pour la supervision des places de parking en temps réel.

---

## 📋 PRÉREQUIS

Avant de commencer, assurez-vous d'avoir installé sur votre machine :

-   **Java (JDK 17+) & Maven** : Pour le Backend Spring Boot.
-   **Node.js & npm** : Pour le Frontend React.
-   **Python (3.8+)** : Pour les scripts d'Intelligence Artificielle.
-   **XAMPP** (ou un serveur MySQL local équivalent) : Pour la base de données.

---

## 🛠️ ÉTAPE 1 : LA BASE DE DONNÉES & LE BACKEND (JAVA)

### 1.1. Préparer la Base de Données

1.  Ouvrez XAMPP et démarrez les modules **Apache** et **MySQL**.
2.  Naviguez vers `http://localhost/phpmyadmin/`.
3.  Créez une nouvelle base de données vide et nommez-la exactement **`smart_parking`**.
    *(Le projet est configuré pour se connecter avec l'utilisateur `root` sans mot de passe, ce qui est le défaut sur XAMPP).*

### 1.2. Lancer le Serveur Spring Boot

1.  Ouvrez le dossier du projet `api` avec votre IDE (IntelliJ IDEA, Eclipse, etc.).
2.  Laissez Maven télécharger toutes les dépendances nécessaires.
3.  Lancez la classe principale `ApiApplication`.
4.  **Vérification** : Le serveur doit démarrer sans erreur et tourner en arrière-plan sur `http://localhost:8080`. Hibernate se chargera de créer automatiquement les tables dans la base de données.

---

## 💻 ÉTAPE 2 : LE FRONTEND (REACT)

1.  Ouvrez un nouveau terminal et placez-vous dans le dossier du projet Frontend (React).
2.  Installez les dépendances du projet avec la commande :
    ```bash
    npm install
    ```
3.  Démarrez le serveur de développement :
    ```bash
    npm run dev
    ```
4.  Ouvrez le lien généré (généralement `http://localhost:5173/`) dans votre navigateur.
5.  **Vérification** : Le tableau de bord du parking s'affiche. Il sera vide tant que le script d'IA n'est pas lancé.

---

## 🧠 ÉTAPE 3 : L'INTELLIGENCE ARTIFICIELLE (PYTHON)

Le système d'IA a été divisé en deux logiques distinctes. L'une est 100% autonome grâce à un surentraînement du modèle, l'autre repose sur une configuration géométrique manuelle.

### 3.1. Créer un Environnement Virtuel (Recommandé)

Pour éviter des conflits de dépendances, il est conseillé d'isoler les bibliothèques Python dans un environnement virtuel.

1.  Ouvrez un terminal à la racine du projet.
2.  Créez l'environnement :
    ```bash
    python -m venv venv
    ```
3.  Activez-le :
    -   **Sur Windows :**
        ```bash
        venv\Scripts\activate
        ```
    -   **Sur macOS / Linux :**
        ```bash
        source venv/bin/activate
        ```

### 3.2. Installation des dépendances Python

Une fois l'environnement activé, installez les bibliothèques requises :

```bash
pip install ultralytics opencv-python requests numpy
```

### 3.3. Méthode A : L'IA 100% Autonome (Dossier `analyse_autonome`)

Cette méthode utilise un modèle surentraîné (`best.pt`) qui reconnaît de lui-même si une place est "libre" ou "occupée". Aucune configuration de zones n'est requise.

1.  Déplacez-vous dans le dossier autonome :
    ```bash
    cd outils/analyse_autonome
    ```
2.  Pour analyser des **photos** (envoie les données au Backend) :
    ```bash
    python analyse_photos.py
    ```
    *(Appuyez sur n'importe quelle touche pour passer à la photo suivante, ou sur 'q' pour quitter).*

3.  Pour analyser une **vidéo en direct** :
    ```bash
    python analyse_live.py
    ```

### 3.4. Méthode B : L'IA Géométrique (Dossier `analyse_avec_places`)

Cette méthode utilise le modèle de base (`yolov8n.pt`) pour détecter uniquement les "voitures", et vérifie mathématiquement si elles sont garées dans des zones que vous dessinez.

1.  Déplacez-vous dans le dossier :
    ```bash
    cd outils/analyse_avec_places
    ```
2.  **Configurer les places** (Optionnel, si `places.json` n'est pas déjà configuré) :
    ```bash
    python definir_places.py
    ```
    *(Cliquez sur les 4 coins de chaque place pour dessiner un polygone. Appuyez sur 's' pour sauvegarder dans `places.json` et quitter).*

3.  **Lancer l'analyse vidéo géométrique** :
    ```bash
    python analyse_video.py
    ```
    *(L'IA analyse la vidéo en direct, utilise un délai anti-clignotement et met à jour le React via le Backend Spring Boot).*
