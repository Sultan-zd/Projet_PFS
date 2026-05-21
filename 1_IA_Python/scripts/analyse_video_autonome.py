"""
============================================================
 Smart Parking Analysis — Analyse Vidéo (Mode Autonome v3.0)
============================================================
 Ce script analyse un flux vidéo en utilisant le modèle IA
 sur-mesure (best.pt) qui classifie directement les places.

 Usage : python analyse_video_autonome.py [video_path]
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
logger = logging.getLogger("AnalyseVideoAutonome")

# ============================================================
#  INITIALISATION
# ============================================================
logger.info("🧠 Initialisation du détecteur autonome (v3.0)...")
detector = ParkingDetector(mode="autonomous")

# Source vidéo (modifier ici ou passer en argument)
video_source = sys.argv[1] if len(sys.argv) > 1 else config.VIDEO_1

if not os.path.exists(video_source):
    logger.error(f"❌ Fichier vidéo introuvable : {video_source}")
    sys.exit(1)

cap = cv2.VideoCapture(video_source)
if not cap.isOpened():
    logger.error(f"❌ Impossible d'ouvrir : {video_source}")
    sys.exit(1)

# Fenêtre d'affichage
window_name = "Smart Parking v3.0 — Analyse Autonome"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)

# Chronomètre d'envoi
last_send_time = time.time()
frame_count = 0
fps_start = time.time()

logger.info(f"▶️  Analyse de : {os.path.basename(video_source)}")
logger.info("   Appuyer sur 'q' pour quitter")

# ============================================================
#  BOUCLE PRINCIPALE
# ============================================================
while True:
    ret, frame = cap.read()
    if not ret:
        logger.info("📼 Fin de la vidéo.")
        break

    # Détection IA (avec prétraitement automatique)
    detections = detector.detect(frame)
    summary = detector.get_summary(detections)

    # FPS
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
            f"Conf moy : {summary['avg_confidence']:.0%} | "
            f"FPS : {fps:.1f}"
        )
        last_send_time = current_time

    # Annotation et affichage
    annotated = detector.draw_results(frame, detections)
    display = cv2.resize(annotated, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
    cv2.imshow(window_name, display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        logger.info("⏹️  Arrêt manuel.")
        break

cap.release()
cv2.destroyAllWindows()

stats = detector.get_detector_stats()
logger.info(f"✅ Analyse terminée — {stats['total_detections']} frames analysés")
