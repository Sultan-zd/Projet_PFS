"""
============================================================
 Smart Parking Analysis — Serveur FastAPI v3.0 (Microservice IA)
============================================================
 Ce serveur expose l'intelligence artificielle comme un
 microservice REST, permettant :
   - L'analyse d'images uploadées depuis l'interface web
   - Le contrôle du flux vidéo en direct
   - La consultation de l'état du serveur IA
   - La calibration des zones de parking
   - Les métriques de précision en temps réel

 Lancement : uvicorn server:app --host 0.0.0.0 --port 8000
============================================================
"""

import io
import os
import sys
import time
import json
import logging
import threading
import numpy as np
from datetime import datetime
from PIL import Image

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config
from scripts.detection_engine import ParkingDetector

# ============================================================
#  Configuration du Logger
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("SmartParkingAPI")

# ============================================================
#  Initialisation FastAPI
# ============================================================
app = FastAPI(
    title="Smart Parking Analysis — AI Engine v3.0",
    description=(
        "Microservice d'intelligence artificielle pour la détection "
        "et l'analyse de places de parking par vision par ordinateur (YOLOv8). "
        "Version 3.0 avec IoU amélioré, prétraitement CLAHE, et anti-flickering intelligent."
    ),
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#  Variables Globales
# ============================================================
detector_autonomous = None
detector_zones = None
server_start_time = None
total_analyses = 0
video_stream_active = False
analysis_history = []  # Historique des analyses récentes


# ============================================================
#  Événements de Démarrage / Arrêt
# ============================================================
@app.on_event("startup")
async def startup_event():
    """Charge les modèles IA au démarrage du serveur (une seule fois)."""
    global detector_autonomous, detector_zones, server_start_time

    server_start_time = datetime.now()
    logger.info("🚀 Démarrage du serveur Smart Parking AI v3.0...")

    try:
        # Charger le détecteur autonome (best.pt)
        if os.path.exists(config.MODEL_CUSTOM_PATH):
            detector_autonomous = ParkingDetector(mode="autonomous")
            logger.info("✅ Détecteur autonome (best.pt) chargé")
        else:
            logger.warning("⚠️ Modèle best.pt non trouvé — mode autonome désactivé")

        # Charger le détecteur avec zones (yolov8m.pt ou yolov8n.pt fallback)
        model_path = config.MODEL_COCO_PATH
        if not os.path.exists(model_path):
            model_path = config.MODEL_COCO_FALLBACK

        if os.path.exists(model_path):
            detector_zones = ParkingDetector(mode="zones")
            model_name = os.path.basename(model_path)
            logger.info(f"✅ Détecteur avec zones ({model_name}) chargé")
        else:
            logger.warning("⚠️ Aucun modèle COCO trouvé — mode zones désactivé")

    except Exception as e:
        logger.error(f"❌ Erreur au chargement des modèles : {e}")

    logger.info("🟢 Serveur Smart Parking AI v3.0 prêt !")


# ============================================================
#  ENDPOINTS — SYSTÈME
# ============================================================

@app.get("/", tags=["Système"])
async def root():
    """Page d'accueil du microservice IA."""
    return {
        "service": "Smart Parking AI Engine",
        "version": "3.0.0",
        "status": "operational",
        "features": [
            "IoU-based detection",
            "CLAHE preprocessing",
            "Anti-flickering (sliding window)",
            "Multi-scale detection",
        ],
        "docs": "/docs"
    }


@app.get("/api/status", tags=["Système"])
async def get_status():
    """
    Retourne l'état actuel du serveur IA avec métriques détaillées.
    Utilisé par le frontend pour vérifier la disponibilité.
    """
    import torch

    uptime = None
    if server_start_time:
        delta = datetime.now() - server_start_time
        uptime = str(delta).split(".")[0]

    # Récupérer les stats des détecteurs
    detector_stats = {}
    if detector_zones:
        detector_stats = detector_zones.get_detector_stats()
    elif detector_autonomous:
        detector_stats = detector_autonomous.get_detector_stats()

    return {
        "status": "operational",
        "version": "3.0.0",
        "uptime": uptime,
        "models": {
            "autonomous": detector_autonomous is not None,
            "zones": detector_zones is not None,
            "model_file": os.path.basename(config.MODEL_COCO_PATH),
        },
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "total_analyses": total_analyses,
        "video_stream_active": video_stream_active,
        "detector_stats": detector_stats,
        "preprocessing": {
            "enabled": config.ENABLE_PREPROCESSING,
            "clahe": True,
            "gamma_correction": True,
            "denoising": config.ENABLE_DENOISING,
        }
    }


# ============================================================
#  ENDPOINTS — ANALYSE
# ============================================================

@app.post("/api/analyze", tags=["Analyse"])
async def analyze_image(
    file: UploadFile = File(...),
    mode: str = Query("autonomous", description="Mode: 'autonomous' ou 'zones'"),
    confidence: float = Query(None, description="Seuil de confiance (0.0-1.0)")
):
    """
    Analyse une image de parking uploadée.

    - **file** : Image du parking (JPEG, PNG)
    - **mode** : `autonomous` (classification directe) ou `zones` (zones prédéfinies)
    - **confidence** : Seuil de confiance optionnel

    Retourne la liste des places détectées avec leur état et score IoU.
    """
    global total_analyses

    # Validation du fichier
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image (JPEG, PNG)")

    # Sélection du détecteur
    if mode == "autonomous":
        detector = detector_autonomous
    elif mode == "zones":
        detector = detector_zones
    else:
        raise HTTPException(status_code=400, detail="Mode invalide. Utilisez 'autonomous' ou 'zones'")

    if detector is None:
        raise HTTPException(
            status_code=503,
            detail=f"Le détecteur en mode '{mode}' n'est pas disponible. Vérifiez que le modèle est présent."
        )

    try:
        # Lire et convertir l'image
        start_time = time.time()
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        frame = np.array(image)
        frame = frame[:, :, ::-1]  # RGB -> BGR pour OpenCV

        # Analyse IA (avec prétraitement automatique)
        detections = detector.detect(frame, confidence=confidence)
        summary = detector.get_summary(detections)
        processing_time = round((time.time() - start_time) * 1000, 1)

        total_analyses += 1

        # Enregistrer dans l'historique
        analysis_entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "processing_time_ms": processing_time,
            "summary": summary,
        }
        analysis_history.append(analysis_entry)
        if len(analysis_history) > 100:
            analysis_history.pop(0)

        logger.info(
            f"📊 Analyse #{total_analyses} ({mode}) — "
            f"{summary['occupied']}/{summary['total']} occupées "
            f"({summary['occupancy_rate']}%) — {processing_time}ms "
            f"— Confiance moy: {summary['avg_confidence']:.0%}"
        )

        return {
            "success": True,
            "mode": mode,
            "processing_time_ms": processing_time,
            "summary": summary,
            "detections": [d.to_dict() for d in detections],
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse : {str(e)}")


@app.post("/api/analyze-batch", tags=["Analyse"])
async def analyze_batch(files: list[UploadFile] = File(...)):
    """
    Analyse un lot d'images de parking.
    Utile pour traiter plusieurs captures d'un coup.
    """
    if not detector_autonomous:
        raise HTTPException(status_code=503, detail="Détecteur non disponible")

    results = []
    for file in files:
        if file.content_type and file.content_type.startswith("image/"):
            try:
                contents = await file.read()
                image = Image.open(io.BytesIO(contents)).convert("RGB")
                frame = np.array(image)[:, :, ::-1]

                detections = detector_autonomous.detect(frame)
                summary = detector_autonomous.get_summary(detections)

                results.append({
                    "filename": file.filename,
                    "summary": summary,
                    "detections": [d.to_dict() for d in detections]
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "error": str(e)
                })

    return {
        "success": True,
        "total_files": len(files),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================
#  ENDPOINTS — CONFIGURATION
# ============================================================

@app.get("/api/zones", tags=["Configuration"])
async def get_zones():
    """
    Retourne la liste des zones de parking configurées (places.json).
    """
    if not os.path.exists(config.PLACES_JSON_PATH):
        return {"zones": [], "message": "Aucune zone configurée"}

    with open(config.PLACES_JSON_PATH, "r") as f:
        zones = json.load(f)

    return {
        "total_zones": len(zones),
        "zones": zones
    }


@app.get("/api/metrics", tags=["Système"])
async def get_metrics():
    """
    Retourne les métriques de performance du système IA.
    """
    return {
        "total_analyses": total_analyses,
        "recent_analyses": analysis_history[-10:] if analysis_history else [],
        "avg_processing_time": (
            round(sum(a["processing_time_ms"] for a in analysis_history) / len(analysis_history), 1)
            if analysis_history else 0
        ),
        "detector_stats": (
            detector_zones.get_detector_stats() if detector_zones
            else detector_autonomous.get_detector_stats() if detector_autonomous
            else {}
        ),
    }


@app.get("/api/config", tags=["Configuration"])
async def get_config():
    """
    Retourne la configuration actuelle du système IA.
    """
    return {
        "confidence_threshold": config.CONFIDENCE_THRESHOLD,
        "iou_threshold": config.IOU_THRESHOLD,
        "zone_overlap_threshold": config.ZONE_OVERLAP_THRESHOLD,
        "anti_flicker_delay": config.ANTI_FLICKER_DELAY_SECONDS,
        "preprocessing": {
            "enabled": config.ENABLE_PREPROCESSING,
            "clahe_clip_limit": config.CLAHE_CLIP_LIMIT,
            "denoising": config.ENABLE_DENOISING,
        },
        "vehicle_classes": config.VEHICLE_CLASSES,
        "multiscale": config.ENABLE_MULTISCALE,
    }


# ============================================================
#  Point d'Entrée
# ============================================================
if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 60)
    logger.info("  Smart Parking Analysis — AI Server v3.0")
    logger.info(f"  URL : http://localhost:{config.FASTAPI_PORT}")
    logger.info(f"  Docs : http://localhost:{config.FASTAPI_PORT}/docs")
    logger.info("=" * 60)

    uvicorn.run(
        "server:app",
        host=config.FASTAPI_HOST,
        port=config.FASTAPI_PORT,
        reload=False,
        log_level="info"
    )
