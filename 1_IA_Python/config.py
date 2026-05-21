"""
============================================================
 Smart Parking Analysis — Configuration Centralisée v3.0
============================================================
 Ce fichier centralise TOUS les paramètres du module IA.
 Modifiez les valeurs ici au lieu de les chercher dans chaque script.
============================================================
"""

import os

# ============================================================
#  CHEMINS DES MODÈLES IA
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Modèle entraîné sur-mesure pour la détection de places (occupied/available)
MODEL_CUSTOM_PATH = os.path.join(BASE_DIR, "modeles", "best.pt")

# Modèle YOLO pré-entraîné — MEDIUM pour meilleure précision
# (yolov8m.pt = 25 Mo, bien plus précis que yolov8n.pt = 6 Mo)
MODEL_COCO_PATH = os.path.join(BASE_DIR, "modeles", "yolov8m.pt")

# Fallback vers le modèle nano si medium non disponible
MODEL_COCO_FALLBACK = os.path.join(BASE_DIR, "modeles", "yolov8n.pt")

# ============================================================
#  CHEMINS DES MÉDIAS
# ============================================================
MEDIA_DIR = os.path.join(BASE_DIR, "medias")
PLACES_JSON_PATH = os.path.join(MEDIA_DIR, "places.json")
PHOTOS_DIR = os.path.join(MEDIA_DIR, "photos_parking")
DATASET_DIR = os.path.join(MEDIA_DIR, "dataset_parking")

# Vidéos de test
VIDEO_DEFAULT = os.path.join(MEDIA_DIR, "parking_video.mp4")
VIDEO_1 = os.path.join(MEDIA_DIR, "parking_video1.mp4")
VIDEO_2 = os.path.join(MEDIA_DIR, "parking_video2.mp4")

# ============================================================
#  PARAMÈTRES D'AFFICHAGE
# ============================================================
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

# ============================================================
#  PARAMÈTRES DE DÉTECTION IA
# ============================================================

# Seuil de confiance minimum pour valider une détection de véhicule
# Abaissé de 0.25 à 0.20 pour capter plus de véhicules (moins de faux négatifs)
CONFIDENCE_THRESHOLD = 0.20

# Seuil de confiance pour l'analyse de photos (plus strict)
CONFIDENCE_THRESHOLD_PHOTOS = 0.50

# Seuil IoU (Intersection over Union) pour la suppression des doublons
IOU_THRESHOLD = 0.45

# Seuil IoU minimum pour considérer qu'un véhicule occupe une place
# Un véhicule qui recouvre au moins 15% de la zone = place occupée
ZONE_OVERLAP_THRESHOLD = 0.15

# Délai anti-flickering : nombre de secondes avant de confirmer qu'une place est libre
# Utilise maintenant une moyenne glissante pondérée
ANTI_FLICKER_DELAY_SECONDS = 8

# Taille de la fenêtre de moyenne glissante pour l'anti-flickering
ANTI_FLICKER_WINDOW_SIZE = 5

# Classes COCO considérées comme des véhicules
# Ajout de 'motorcycle' pour les deux-roues
VEHICLE_CLASSES = ["car", "truck", "bus", "motorcycle"]

# ============================================================
#  PARAMÈTRES DE PRÉTRAITEMENT D'IMAGE
# ============================================================

# Activer le prétraitement automatique (CLAHE + correction gamma)
ENABLE_PREPROCESSING = True

# CLAHE (Contrast Limited Adaptive Histogram Equalization)
CLAHE_CLIP_LIMIT = 2.5
CLAHE_TILE_SIZE = (8, 8)

# Correction gamma automatique
# Si la luminosité moyenne < ce seuil → appliquer correction gamma
BRIGHTNESS_LOW_THRESHOLD = 80
BRIGHTNESS_HIGH_THRESHOLD = 200
GAMMA_DARK = 1.4      # Éclaircir les images sombres
GAMMA_BRIGHT = 0.8    # Assombrir les images trop claires

# Réduction de bruit (filtre bilatéral)
ENABLE_DENOISING = True
DENOISE_STRENGTH = 5

# ============================================================
#  PARAMÈTRES DE DÉTECTION MULTI-ÉCHELLE
# ============================================================

# Activer la détection multi-échelle (plus lent mais plus précis)
ENABLE_MULTISCALE = False

# Tailles d'images pour la détection multi-échelle
MULTISCALE_SIZES = [640, 1280]

# ============================================================
#  COMMUNICATION AVEC LE BACKEND SPRING BOOT
# ============================================================
SPRING_BOOT_API_URL = "http://localhost:8080/api/parking/update"
SPRING_BOOT_BATCH_URL = "http://localhost:8080/api/parking/update-batch"

# Intervalle d'envoi des données au backend (en secondes)
SEND_INTERVAL_SECONDS = 3.0

# Timeout pour les requêtes HTTP vers Spring Boot
HTTP_TIMEOUT_SECONDS = 1.0

# ============================================================
#  PARAMÈTRES DU SERVEUR FASTAPI
# ============================================================
FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = 8000

# ============================================================
#  PARAMÈTRES D'ENTRAÎNEMENT (Option B — PKLot)
# ============================================================
TRAINING_EPOCHS = 100          # Plus d'epochs pour un meilleur apprentissage
TRAINING_IMAGE_SIZE = 640
TRAINING_BATCH_SIZE = 16       # Ajuster selon votre GPU (8 si peu de VRAM)
TRAINING_PATIENCE = 15         # Early stopping si pas d'amélioration
TRAINING_DATA_YAML = os.path.join(DATASET_DIR, "data.yaml")

# Modèle de base pour l'entraînement (medium pour meilleure qualité)
TRAINING_BASE_MODEL = "yolov8m.pt"

# Data augmentation avancée
TRAINING_AUGMENTATION = {
    "hsv_h": 0.015,           # Variation de teinte
    "hsv_s": 0.7,             # Variation de saturation
    "hsv_v": 0.4,             # Variation de luminosité
    "degrees": 0.0,           # Pas de rotation (les parkings sont fixes)
    "translate": 0.1,         # Légère translation
    "scale": 0.3,             # Variation d'échelle
    "shear": 0.0,             # Pas de cisaillement
    "flipud": 0.0,            # Pas de flip vertical
    "fliplr": 0.5,            # Flip horizontal
    "mosaic": 1.0,            # Mosaïque (très efficace)
    "mixup": 0.1,             # Mixup (mélange d'images)
    "copy_paste": 0.1,        # Copy-paste augmentation
}

# ============================================================
#  PKLOT DATASET
# ============================================================
PKLOT_DATASET_DIR = os.path.join(MEDIA_DIR, "pklot_dataset")
PKLOT_DATA_YAML = os.path.join(PKLOT_DATASET_DIR, "data.yaml")
