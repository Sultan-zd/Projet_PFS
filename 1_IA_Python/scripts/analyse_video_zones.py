"""
============================================================
 Smart Parking Analysis — Analyse Vidéo (Mode Zones v3.0)
============================================================
 Ce script analyse un flux vidéo en vérifiant la présence de
 véhicules dans des zones prédéfinies (places.json).
 
 Améliorations v3.0 :
   - Prétraitement CLAHE automatique
   - Détection IoU (Intersection over Union)
   - Anti-flickering par moyenne glissante
   - HUD avec métriques en temps réel

 Usage : python analyse_video_zones.py [video_path]
============================================================
"""

import cv2
import time
import logging
import requests
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from scripts.detection_engine import ParkingDetector

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("AnalyseVideoZones")

# ============================================================
#  INITIALISATION
# ============================================================
logger.info("🧠 Initialisation du détecteur avec zones prédéfinies (v3.0)...")
detector = ParkingDetector(mode="zones")

video_source = sys.argv[1] if len(sys.argv) > 1 else config.VIDEO_DEFAULT

if not os.path.exists(video_source):
    logger.error(f"❌ Fichier vidéo introuvable : {video_source}")
    sys.exit(1)

cap = cv2.VideoCapture(video_source)
if not cap.isOpened():
    logger.error(f"❌ Impossible d'ouvrir : {video_source}")
    sys.exit(1)

# Fenêtre d'affichage
window_name = "Smart Parking v3.0 — Zones + IoU + CLAHE"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)

last_send_time = time.time()
frame_count = 0
fps_start = time.time()

logger.info(f"▶️  Analyse de : {os.path.basename(video_source)}")
logger.info(f"   Anti-flickering : {config.ANTI_FLICKER_DELAY_SECONDS}s (moyenne glissante)")
logger.info(f"   Prétraitement   : {'CLAHE + Gamma' if config.ENABLE_PREPROCESSING else 'Désactivé'}")
logger.info("   Appuyer sur 'q' pour quitter")

# ============================================================
#  BOUCLE PRINCIPALE
# ============================================================
while True:
    ret, frame_full = cap.read()
    if not ret:
        logger.info("📼 Fin de la vidéo — Rebobinage...")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Redimensionner pour l'analyse
    frame = cv2.resize(frame_full, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))

    # Détection IA (avec prétraitement automatique intégré)
    detections = detector.detect(frame)
    summary = detector.get_summary(detections)

    # Calcul FPS
    frame_count += 1
    elapsed = time.time() - fps_start
    fps = frame_count / elapsed if elapsed > 0 else 0

    # Envoi périodique à Spring Boot
    current_time = time.time()
    if (current_time - last_send_time) > config.SEND_INTERVAL_SECONDS:
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
            f"📊 {summary['available']} Libres | "
            f"{summary['occupied']} Occupées | "
            f"Taux : {summary['occupancy_rate']}% | "
            f"Véhicules : {summary['vehicles_detected']} | "
            f"Conf moy : {summary['avg_confidence']:.0%} | "
            f"FPS : {fps:.1f}"
        )
        last_send_time = current_time

    # Annotation et affichage
    annotated = detector.draw_results(frame, detections)

    # Ajouter FPS au HUD
    cv2.putText(annotated, f"FPS: {fps:.1f}", (config.DISPLAY_WIDTH - 120, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

    cv2.imshow(window_name, annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        logger.info("⏹️  Arrêt manuel.")
        break

cap.release()
cv2.destroyAllWindows()

# Stats finales
stats = detector.get_detector_stats()
logger.info("=" * 50)
logger.info(f"✅ Analyse terminée — {stats['total_detections']} frames analysés")
logger.info(f"   Prétraitement : {stats['preprocessing_stats']}")
logger.info("=" * 50)
