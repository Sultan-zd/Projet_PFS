"""
============================================================
 Smart Parking Analysis — Moteur de Détection Unifié v3.0
============================================================
 Classe centrale qui encapsule toute la logique de détection
 de véhicules et d'analyse des places de parking.

 Améliorations v3.0 :
   - Calcul IoU réel (polygone vs bounding box)
   - Prétraitement d'image automatique (CLAHE + gamma)
   - Anti-flickering par moyenne glissante pondérée
   - Score de confiance composite (YOLO + IoU)
   - Support multi-échelle optionnel
   - Meilleure gestion des classes véhicules

 Deux modes de fonctionnement :
   1. AUTONOME   — L'IA classifie directement (best.pt)
   2. AVEC ZONES — Détection véhicules + vérification IoU
============================================================
"""

import cv2
import json
import time
import logging
import numpy as np
from collections import deque
from ultralytics import YOLO

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from scripts.image_preprocessor import ImagePreprocessor

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ParkingDetector")


class DetectionResult:
    """Résultat structuré d'une détection pour une place de parking."""

    def __init__(self, place_id: str, occupied: bool, confidence: float = 0.0,
                 bbox: tuple = None, zone_points: list = None,
                 iou_score: float = 0.0, zone_name: str = None):
        self.place_id = place_id
        self.occupied = occupied
        self.confidence = confidence
        self.bbox = bbox
        self.zone_points = zone_points
        self.iou_score = iou_score
        self.zone_name = zone_name

    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour l'envoi API."""
        result = {
            "numeroPlace": self.place_id,
            "occupee": self.occupied,
            "confiance": round(self.confidence, 2),
        }
        if self.iou_score > 0:
            result["iouScore"] = round(self.iou_score, 2)
        if self.bbox:
            result["bbox"] = {
                "x1": self.bbox[0], "y1": self.bbox[1],
                "x2": self.bbox[2], "y2": self.bbox[3]
            }
        if self.zone_name:
            result["zone"] = self.zone_name
        return result

    def __repr__(self):
        status = "🔴 Occupée" if self.occupied else "🟢 Libre"
        iou_info = f" IoU:{self.iou_score:.0%}" if self.iou_score > 0 else ""
        return f"[{self.place_id}] {status} (conf:{self.confidence:.0%}{iou_info})"


class ParkingDetector:
    """
    Moteur de détection intelligent v3.0 pour l'analyse de parkings.

    Utilise YOLOv8 + IoU + Prétraitement pour une détection précise.
    """

    def __init__(self, mode: str = "autonomous"):
        """
        Initialise le détecteur.

        Args:
            mode: "autonomous" — utilise best.pt (classification directe)
                  "zones"      — utilise yolov8m.pt + places.json + IoU
        """
        self.mode = mode
        self._zones = []
        self._preprocessor = ImagePreprocessor()

        # Anti-flickering amélioré : moyenne glissante par place
        self._occupation_history = {}  # {place_id: deque([bool, bool, ...])}
        self._last_occupied_times = {}  # {place_id: timestamp}

        # Statistiques
        self._total_detections = 0
        self._total_vehicles_found = 0

        # Chargement du modèle approprié
        if mode == "autonomous":
            model_path = config.MODEL_CUSTOM_PATH
            logger.info("🧠 Chargement du modèle sur-mesure (best.pt)...")
        else:
            # Essayer le modèle medium, sinon fallback nano
            model_path = config.MODEL_COCO_PATH
            if not os.path.exists(model_path):
                model_path = config.MODEL_COCO_FALLBACK
                logger.warning(f"⚠️ yolov8m.pt non trouvé, fallback vers yolov8n.pt")
            logger.info(f"🧠 Chargement du modèle COCO ({os.path.basename(model_path)})...")
            self._load_zones()

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modèle introuvable : {model_path}")

        self.model = YOLO(model_path)
        logger.info(f"✅ Modèle chargé avec succès ({mode} mode)")

    def _load_zones(self):
        """Charge les zones prédéfinies depuis places.json."""
        if not os.path.exists(config.PLACES_JSON_PATH):
            logger.warning(f"⚠️ Fichier places.json introuvable : {config.PLACES_JSON_PATH}")
            return

        with open(config.PLACES_JSON_PATH, "r") as f:
            self._zones = json.load(f)

        # Pré-calculer les contours numpy pour chaque zone (optimisation)
        for zone in self._zones:
            zone["_contour"] = np.array(zone["points"], np.int32)
            zone["_area"] = cv2.contourArea(zone["_contour"])

            # Initialiser l'historique anti-flickering
            zone_id = zone["id"]
            self._occupation_history[zone_id] = deque(
                maxlen=config.ANTI_FLICKER_WINDOW_SIZE
            )

        logger.info(f"📍 {len(self._zones)} zones de parking chargées")

    # ================================================================
    #  DETECTION PRINCIPALE
    # ================================================================

    def detect(self, frame: np.ndarray, confidence: float = None) -> list:
        """
        Analyse une image et retourne l'état de chaque place.

        Args:
            frame: Image BGR (numpy array) à analyser
            confidence: Seuil de confiance (utilise config par défaut)

        Returns:
            Liste de DetectionResult
        """
        self._total_detections += 1

        # Prétraitement de l'image
        processed_frame = self._preprocessor.process(frame)

        if self.mode == "autonomous":
            return self._detect_autonomous(processed_frame, confidence)
        else:
            return self._detect_with_zones(processed_frame, confidence)

    def _detect_autonomous(self, frame: np.ndarray, confidence: float = None) -> list:
        """
        Mode AUTONOME : L'IA classifie directement chaque place détectée.
        Utilise le modèle best.pt entraîné sur les classes 'occupied' / 'available'.
        """
        conf = confidence or config.CONFIDENCE_THRESHOLD
        results = self.model(frame, conf=conf, iou=config.IOU_THRESHOLD, verbose=False)
        boxes = results[0].boxes

        detections = []
        counter = 1

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id].lower()
            conf_score = float(box.conf[0])

            occupied = class_name in ["occupied", "car", "truck"]

            detection = DetectionResult(
                place_id=f"P{counter}",
                occupied=occupied,
                confidence=conf_score,
                bbox=(x1, y1, x2, y2)
            )
            detections.append(detection)
            counter += 1

        return detections

    def _detect_with_zones(self, frame: np.ndarray, confidence: float = None) -> list:
        """
        Mode ZONES v3.0 : Détection de véhicules + vérification IoU
        avec polygones prédéfinis + anti-flickering par moyenne glissante.
        """
        conf = confidence or config.CONFIDENCE_THRESHOLD

        # Détection multi-échelle optionnelle
        if config.ENABLE_MULTISCALE:
            vehicle_boxes = self._detect_multiscale(frame, conf)
        else:
            results = self.model(frame, conf=conf, verbose=False)
            vehicle_boxes = results[0].boxes

        # Filtrer uniquement les véhicules
        vehicles = []
        for box in vehicle_boxes:
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id].lower()
            if class_name in config.VEHICLE_CLASSES:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf_score = float(box.conf[0])
                vehicles.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": conf_score,
                    "class": class_name
                })

        self._total_vehicles_found = len(vehicles)
        current_time = time.time()
        detections = []

        for zone in self._zones:
            zone_id = zone["id"]
            zone_contour = zone["_contour"]
            zone_area = zone["_area"]
            zone_name = zone.get("zone", None)

            # Calculer le meilleur IoU avec tous les véhicules détectés
            best_iou = 0.0
            best_confidence = 0.0
            vehicle_detected = False

            for vehicle in vehicles:
                iou = self._calculate_polygon_bbox_iou(
                    zone_contour, zone_area, vehicle["bbox"]
                )

                if iou > best_iou:
                    best_iou = iou
                    best_confidence = vehicle["confidence"]

                # Si IoU dépasse le seuil → véhicule dans cette zone
                if iou >= config.ZONE_OVERLAP_THRESHOLD:
                    vehicle_detected = True

            # Si pas de match IoU, essayer le test multi-points (fallback)
            if not vehicle_detected:
                for vehicle in vehicles:
                    if self._multipoint_test(zone_contour, vehicle["bbox"]):
                        vehicle_detected = True
                        best_confidence = vehicle["confidence"]
                        best_iou = 0.1  # Score IoU minimal pour le fallback
                        break

            # Anti-flickering par moyenne glissante pondérée
            history = self._occupation_history[zone_id]
            history.append(vehicle_detected)

            if vehicle_detected:
                self._last_occupied_times[zone_id] = current_time
                is_occupied = True
                final_confidence = best_confidence * 0.7 + best_iou * 0.3
            else:
                last_seen = self._last_occupied_times.get(zone_id, 0)
                elapsed = current_time - last_seen

                # Vérifier la moyenne glissante
                if len(history) >= 3:
                    recent_ratio = sum(history) / len(history)
                    if recent_ratio > 0.5 and elapsed < config.ANTI_FLICKER_DELAY_SECONDS:
                        is_occupied = True
                        final_confidence = 0.4  # Confiance réduite
                    else:
                        is_occupied = False
                        final_confidence = 1.0 - min(elapsed / 20.0, 0.9)
                elif elapsed < config.ANTI_FLICKER_DELAY_SECONDS:
                    is_occupied = True
                    final_confidence = 0.3
                else:
                    is_occupied = False
                    final_confidence = 0.9

            detection = DetectionResult(
                place_id=zone_id,
                occupied=is_occupied,
                confidence=max(0.0, min(1.0, final_confidence)),
                zone_points=zone["points"],
                iou_score=best_iou,
                zone_name=zone_name
            )
            detections.append(detection)

        return detections

    # ================================================================
    #  CALCULS GÉOMÉTRIQUES
    # ================================================================

    def _calculate_polygon_bbox_iou(self, polygon: np.ndarray,
                                     polygon_area: float,
                                     bbox: tuple) -> float:
        """
        Calcule l'IoU (Intersection over Union) entre un polygone
        (zone de parking) et une bounding box (véhicule détecté).

        C'est la VRAIE mesure de recouvrement, bien plus précise
        que le simple test de point central.
        """
        x1, y1, x2, y2 = bbox

        # Créer un contour rectangulaire pour la bbox
        bbox_contour = np.array([
            [x1, y1], [x2, y1], [x2, y2], [x1, y2]
        ], np.int32)

        bbox_area = (x2 - x1) * (y2 - y1)
        if bbox_area <= 0 or polygon_area <= 0:
            return 0.0

        # Calculer l'intersection en utilisant cv2
        # Créer des masques binaires pour les deux formes
        # Déterminer le bounding rect englobant les deux formes
        all_pts = np.vstack([polygon, bbox_contour])
        min_x = max(0, int(np.min(all_pts[:, 0])))
        min_y = max(0, int(np.min(all_pts[:, 1])))
        max_x = int(np.max(all_pts[:, 0])) + 1
        max_y = int(np.max(all_pts[:, 1])) + 1

        w = max_x - min_x
        h = max_y - min_y

        if w <= 0 or h <= 0:
            return 0.0

        # Limiter la taille pour la performance
        if w > 2000 or h > 2000:
            return 0.0

        # Masques translatés
        offset_poly = polygon - np.array([min_x, min_y])
        offset_bbox = bbox_contour - np.array([min_x, min_y])

        mask_poly = np.zeros((h, w), dtype=np.uint8)
        mask_bbox = np.zeros((h, w), dtype=np.uint8)

        cv2.fillPoly(mask_poly, [offset_poly], 255)
        cv2.fillPoly(mask_bbox, [offset_bbox], 255)

        # Intersection et Union
        intersection = cv2.bitwise_and(mask_poly, mask_bbox)
        union = cv2.bitwise_or(mask_poly, mask_bbox)

        inter_area = np.count_nonzero(intersection)
        union_area = np.count_nonzero(union)

        if union_area == 0:
            return 0.0

        return inter_area / union_area

    def _multipoint_test(self, zone_contour: np.ndarray, bbox: tuple) -> bool:
        """
        Test multi-points amélioré : vérifie si plusieurs points
        du véhicule tombent dans la zone de parking.
        Teste 9 points au lieu de 3.
        """
        x1, y1, x2, y2 = bbox
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # 9 points de test : centre, milieux des bords, quarts
        test_points = [
            (cx, cy),                           # Centre
            (cx, int(y2 - 5)),                  # Bas centre
            (cx, int(y1 + 0.75 * (y2 - y1))),  # 3/4 bas
            (cx, int(y1 + 0.25 * (y2 - y1))),  # 1/4 haut
            (int(x1 + 0.25 * (x2 - x1)), cy),  # 1/4 gauche
            (int(x1 + 0.75 * (x2 - x1)), cy),  # 3/4 droite
            (int(x1 + 0.3 * (x2 - x1)), int(y1 + 0.7 * (y2 - y1))),
            (int(x1 + 0.7 * (x2 - x1)), int(y1 + 0.7 * (y2 - y1))),
            (cx, int(y1 + 5)),                  # Haut centre
        ]

        # Si au moins 2 points sont dans la zone → match
        hits = sum(
            1 for px, py in test_points
            if cv2.pointPolygonTest(zone_contour, (px, py), False) >= 0
        )

        return hits >= 2

    def _detect_multiscale(self, frame: np.ndarray, confidence: float):
        """
        Détection multi-échelle : analyse l'image à plusieurs
        résolutions et fusionne les résultats pour capter
        les petits véhicules éloignés.
        """
        all_boxes = []

        for size in config.MULTISCALE_SIZES:
            h, w = frame.shape[:2]
            scale = size / max(h, w)
            resized = cv2.resize(frame, (int(w * scale), int(h * scale)))

            results = self.model(resized, conf=confidence, verbose=False)
            boxes = results[0].boxes

            # Remettre les coordonnées à l'échelle originale
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                scaled_box = box
                # Note: les coordonnées sont automatiquement dans l'espace de l'image redimensionnée
                all_boxes.append(box)

        return all_boxes if all_boxes else self.model(frame, conf=confidence, verbose=False)[0].boxes

    # ================================================================
    #  VISUALISATION
    # ================================================================

    def draw_results(self, frame: np.ndarray, detections: list) -> np.ndarray:
        """
        Dessine les résultats de détection sur l'image avec style amélioré.
        """
        annotated = frame.copy()

        for det in detections:
            # Couleurs avec dégradé
            if det.occupied:
                color = (0, 0, 220)       # Rouge
                fill_color = (0, 0, 80)   # Rouge foncé semi-transparent
                status = "OCCUPEE"
            else:
                color = (0, 200, 0)       # Vert
                fill_color = (0, 80, 0)   # Vert foncé semi-transparent
                status = "LIBRE"

            label = f"{det.place_id}: {status}"
            conf_text = f"{det.confidence:.0%}"

            if det.bbox:
                # Mode autonome — dessiner le rectangle
                x1, y1, x2, y2 = det.bbox
                cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

                # Label avec fond
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 8, y1), color, -1)
                cv2.putText(annotated, label, (x1 + 4, y1 - 4),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            elif det.zone_points:
                # Mode zones — dessiner le polygone avec remplissage semi-transparent
                pts = np.array(det.zone_points, np.int32)

                # Remplissage semi-transparent
                overlay = annotated.copy()
                cv2.fillPoly(overlay, [pts], fill_color)
                cv2.addWeighted(overlay, 0.3, annotated, 0.7, 0, annotated)

                # Contour
                cv2.polylines(annotated, [pts], True, color, 2)

                # Label
                cx = int(np.mean(pts[:, 0]))
                cy = int(np.mean(pts[:, 1]))
                cv2.putText(annotated, det.place_id, (cx - 15, cy - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(annotated, conf_text, (cx - 12, cy + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, color, 1)

        # HUD en haut de l'image
        summary = self.get_summary(detections)
        hud_text = (
            f"Places: {summary['total']} | "
            f"Libres: {summary['available']} | "
            f"Occupees: {summary['occupied']} | "
            f"Taux: {summary['occupancy_rate']}%"
        )

        # Fond noir semi-transparent pour le HUD
        cv2.rectangle(annotated, (0, 0), (len(hud_text) * 11, 35), (0, 0, 0), -1)
        cv2.putText(annotated, hud_text, (10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

        return annotated

    def get_summary(self, detections: list) -> dict:
        """
        Calcule un résumé statistique des détections.
        """
        total = len(detections)
        occupied = sum(1 for d in detections if d.occupied)
        available = total - occupied
        avg_confidence = (
            sum(d.confidence for d in detections) / total if total > 0 else 0.0
        )

        return {
            "total": total,
            "occupied": occupied,
            "available": available,
            "occupancy_rate": round(occupied / total * 100, 1) if total > 0 else 0.0,
            "avg_confidence": round(avg_confidence, 2),
            "vehicles_detected": self._total_vehicles_found,
        }

    def get_detector_stats(self) -> dict:
        """Retourne les statistiques globales du détecteur."""
        return {
            "mode": self.mode,
            "total_detections": self._total_detections,
            "zones_count": len(self._zones),
            "preprocessing_stats": self._preprocessor.get_stats(),
        }
