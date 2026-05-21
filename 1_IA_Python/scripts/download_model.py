"""
============================================================
 Smart Parking — Téléchargement du Modèle YOLOv8 Medium
============================================================
 Ce script télécharge automatiquement le modèle yolov8m.pt
 (25 Mo) qui est bien plus précis que yolov8n.pt (6 Mo).

 Usage : python download_model.py
============================================================
"""

import os
import sys
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("DownloadModel")


def download_yolov8m():
    """Télécharge yolov8m.pt via l'API Ultralytics."""
    from ultralytics import YOLO

    target_path = config.MODEL_COCO_PATH
    model_dir = os.path.dirname(target_path)

    if os.path.exists(target_path):
        size_mb = os.path.getsize(target_path) / (1024 * 1024)
        logger.info(f"✅ yolov8m.pt déjà présent ({size_mb:.1f} Mo)")
        return True

    logger.info("=" * 60)
    logger.info("  Téléchargement du modèle YOLOv8 Medium")
    logger.info("=" * 60)
    logger.info(f"  Destination : {target_path}")
    logger.info("  Taille estimée : ~25 Mo")
    logger.info("  Ce modèle est 3x plus précis que yolov8n")
    logger.info("=" * 60)

    try:
        # Ultralytics télécharge automatiquement le modèle
        logger.info("📥 Téléchargement en cours...")
        model = YOLO("yolov8m.pt")

        # Le modèle est téléchargé dans le répertoire courant par défaut
        # On le déplace vers notre dossier modeles/
        default_path = os.path.join(os.getcwd(), "yolov8m.pt")

        if os.path.exists(default_path):
            os.makedirs(model_dir, exist_ok=True)
            os.rename(default_path, target_path)
            size_mb = os.path.getsize(target_path) / (1024 * 1024)
            logger.info(f"✅ Modèle téléchargé et déplacé ({size_mb:.1f} Mo)")
        elif os.path.exists(target_path):
            logger.info("✅ Modèle déjà en place")
        else:
            # Chercher dans le cache Ultralytics
            import shutil
            home = os.path.expanduser("~")
            cache_path = os.path.join(home, ".cache", "ultralytics", "yolov8m.pt")
            if not os.path.exists(cache_path):
                # Essayer un autre emplacement
                for root, dirs, files in os.walk(os.path.join(home, ".cache")):
                    for f in files:
                        if f == "yolov8m.pt":
                            cache_path = os.path.join(root, f)
                            break

            if os.path.exists(cache_path):
                os.makedirs(model_dir, exist_ok=True)
                shutil.copy2(cache_path, target_path)
                size_mb = os.path.getsize(target_path) / (1024 * 1024)
                logger.info(f"✅ Modèle copié depuis le cache ({size_mb:.1f} Mo)")
            else:
                logger.warning("⚠️ Impossible de localiser le modèle téléchargé")
                logger.info("   Essayez : pip install ultralytics && yolo export model=yolov8m.pt")
                return False

        return True

    except Exception as e:
        logger.error(f"❌ Erreur lors du téléchargement : {e}")
        logger.info("   Vérifiez votre connexion Internet")
        return False


if __name__ == "__main__":
    success = download_yolov8m()
    if success:
        logger.info("🎉 Modèle prêt ! Vous pouvez maintenant utiliser le détecteur amélioré.")
    else:
        logger.error("❌ Échec du téléchargement. Le système utilisera yolov8n.pt en fallback.")
