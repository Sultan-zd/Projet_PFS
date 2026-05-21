"""
============================================================
 Smart Parking Analysis — Analyse de Photos v3.0
============================================================
 Ce script analyse toutes les images d'un dossier et envoie
 les résultats au backend Spring Boot.

 Usage : python analyse_photos.py [dossier_photos]
============================================================
"""

import cv2
import logging
import requests
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from scripts.detection_engine import ParkingDetector

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("AnalysePhotos")

# ============================================================
#  INITIALISATION
# ============================================================
logger.info("🧠 Initialisation du détecteur autonome (v3.0)...")
detector = ParkingDetector(mode="autonomous")

photos_dir = sys.argv[1] if len(sys.argv) > 1 else config.PHOTOS_DIR

if not os.path.exists(photos_dir):
    logger.error(f"❌ Dossier introuvable : {photos_dir}")
    logger.info("   Créez le dossier et ajoutez vos images (.jpg, .png)")
    sys.exit(1)

# Récupérer les fichiers images
image_files = [
    f for f in sorted(os.listdir(photos_dir))
    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
]

if not image_files:
    logger.error(f"❌ Aucune image trouvée dans : {photos_dir}")
    sys.exit(1)

# Fenêtre d'affichage
window_name = "Smart Parking v3.0 — Analyse de Photos"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)

logger.info(f"📸 {len(image_files)} images à analyser")
logger.info("   Appuyer sur une touche pour passer à l'image suivante")
logger.info("   Appuyer sur 'q' pour quitter")
logger.info("=" * 50)

# ============================================================
#  BOUCLE D'ANALYSE
# ============================================================
for i, filename in enumerate(image_files, 1):
    filepath = os.path.join(photos_dir, filename)
    frame = cv2.imread(filepath)

    if frame is None:
        logger.warning(f"⚠️ Impossible de lire : {filename}")
        continue

    logger.info(f"[{i}/{len(image_files)}] Analyse de : {filename}")

    # Détection IA (avec prétraitement automatique)
    detections = detector.detect(frame, confidence=config.CONFIDENCE_THRESHOLD_PHOTOS)
    summary = detector.get_summary(detections)

    # Envoi immédiat à Spring Boot
    for det in detections:
        try:
            requests.post(
                config.SPRING_BOOT_API_URL,
                json=det.to_dict(),
                timeout=config.HTTP_TIMEOUT_SECONDS
            )
        except requests.exceptions.RequestException:
            pass

    logger.info(
        f"   → {summary['available']} Libres | "
        f"{summary['occupied']} Occupées | "
        f"Taux : {summary['occupancy_rate']}% | "
        f"Confiance moy : {summary['avg_confidence']:.0%}"
    )

    # Annotation et affichage
    annotated = detector.draw_results(frame, detections)
    display = cv2.resize(annotated, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
    cv2.imshow(window_name, display)

    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        logger.info("⏹️  Arrêt manuel.")
        break

cv2.destroyAllWindows()

stats = detector.get_detector_stats()
logger.info(f"✅ Analyse terminée — {stats['total_detections']} photos analysées")
logger.info(f"   Prétraitement : {stats['preprocessing_stats']}")
