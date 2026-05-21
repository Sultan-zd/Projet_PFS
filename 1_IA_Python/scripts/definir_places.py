"""
============================================================
 Smart Parking Analysis — Outil de Configuration des Places
============================================================
 Outil interactif pour définir les zones de parking sur une
 image de référence. Les zones sont sauvegardées en JSON.

 Contrôles :
   - Clic gauche   : Placer un point (4 points = 1 place)
   - Touche 'z'    : Annuler la dernière place enregistrée
   - Touche 's'    : Sauvegarder et quitter
   - Touche 'q'    : Quitter sans sauvegarder

 Usage : python definir_places.py [video_ou_image]
============================================================
"""

import cv2
import json
import logging
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("ConfigPlaces")

# ============================================================
#  VARIABLES
# ============================================================
places = []
current_points = []
place_counter = 1
frame_display = None

# ============================================================
#  CALLBACKS SOURIS
# ============================================================
def mouse_callback(event, x, y, flags, param):
    global current_points, place_counter, frame_display

    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append([x, y])
        cv2.circle(frame_display, (x, y), 5, (0, 0, 255), -1)

        # Si 4 points placés → fermer le polygone
        if len(current_points) == 4:
            pts = np.array(current_points, np.int32)
            cv2.polylines(frame_display, [pts], True, (0, 255, 0), 2)
            cv2.putText(
                frame_display, f"P{place_counter}",
                (current_points[0][0], current_points[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
            )

            places.append({
                "id": f"P{place_counter}",
                "points": current_points.copy()
            })

            logger.info(f"✅ Place P{place_counter} enregistrée ({len(places)} au total)")
            place_counter += 1
            current_points = []

        cv2.imshow("Configuration des Places", frame_display)

# ============================================================
#  CHARGEMENT DE L'IMAGE DE RÉFÉRENCE
# ============================================================
source = sys.argv[1] if len(sys.argv) > 1 else config.VIDEO_DEFAULT

if source.lower().endswith(('.jpg', '.jpeg', '.png')):
    frame = cv2.imread(source)
else:
    cap = cv2.VideoCapture(source)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        logger.error(f"❌ Impossible de lire : {source}")
        sys.exit(1)

frame = cv2.resize(frame, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
frame_display = frame.copy()

# ============================================================
#  INTERFACE
# ============================================================
cv2.namedWindow("Configuration des Places")
cv2.setMouseCallback("Configuration des Places", mouse_callback)

logger.info("=" * 55)
logger.info("🛠️  OUTIL DE CONFIGURATION DES PLACES DE PARKING")
logger.info("=" * 55)
logger.info("  Pour CHAQUE place : Cliquez sur les 4 coins")
logger.info("  (dans le sens horaire ou anti-horaire)")
logger.info("")
logger.info("  [s] → Sauvegarder et quitter")
logger.info("  [z] → Annuler la dernière place")
logger.info("  [q] → Quitter SANS sauvegarder")
logger.info("=" * 55)

cv2.imshow("Configuration des Places", frame_display)

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        with open(config.PLACES_JSON_PATH, 'w') as f:
            json.dump(places, f, indent=4)
        logger.info(f"💾 {len(places)} places sauvegardées dans places.json")
        break

    elif key == ord('z'):
        if places:
            removed = places.pop()
            place_counter -= 1
            logger.info(f"↩️  Place {removed['id']} supprimée")
            # Redessiner tout
            frame_display = frame.copy()
            for p in places:
                pts = np.array(p["points"], np.int32)
                cv2.polylines(frame_display, [pts], True, (0, 255, 0), 2)
                cv2.putText(
                    frame_display, p["id"],
                    (p["points"][0][0], p["points"][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                )
            cv2.imshow("Configuration des Places", frame_display)

    elif key == ord('q'):
        logger.info("🚫 Annulation — Aucune sauvegarde.")
        break

cv2.destroyAllWindows()
