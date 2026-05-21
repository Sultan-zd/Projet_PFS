"""
============================================================
 Smart Parking Analysis — Entraînement du Modèle IA v3.0
============================================================
 Ce script entraîne un modèle YOLOv8 MEDIUM sur votre dataset
 avec data augmentation avancée et early stopping.

 Améliorations v3.0 :
   - Modèle de base : yolov8m (au lieu de yolov8n)
   - Data augmentation avancée (HSV, mosaïque, mixup)
   - Early stopping (arrêt si pas d'amélioration)
   - Support GPU automatique (CUDA si disponible)
   - Métriques détaillées et matrice de confusion
   - Export optimisé du meilleur modèle

 Prérequis :
   - Dataset dans medias/dataset_parking/ (format YOLO)
   - GPU NVIDIA avec CUDA (recommandé) ou CPU (lent)

 Usage :
   python entrainer_ia.py              # 100 epochs (défaut)
   python entrainer_ia.py 50           # 50 epochs
   python entrainer_ia.py 100 --resume # Reprendre un entraînement
============================================================
"""

import sys
import os
import shutil
import logging
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

from ultralytics import YOLO

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("EntrainementIA")

# ============================================================
#  CONFIGURATION
# ============================================================
epochs = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else config.TRAINING_EPOCHS
resume = "--resume" in sys.argv

# Déterminer le dataset à utiliser
merged_yaml = os.path.join(config.MEDIA_DIR, "merged_dataset", "data.yaml")
if os.path.exists(merged_yaml):
    data_yaml = merged_yaml
    dataset_name = "Merged (Existant + PKLot)"
elif os.path.exists(config.PKLOT_DATA_YAML):
    data_yaml = config.PKLOT_DATA_YAML
    dataset_name = "PKLot"
elif os.path.exists(config.TRAINING_DATA_YAML):
    data_yaml = config.TRAINING_DATA_YAML
    dataset_name = "Existant (Roboflow)"
else:
    logger.error(f"❌ Aucun dataset trouvé !")
    logger.info(f"   Attendu dans : {config.TRAINING_DATA_YAML}")
    logger.info(f"   Exécutez d'abord : python prepare_dataset.py")
    sys.exit(1)

# Déterminer le modèle de base
base_model = config.TRAINING_BASE_MODEL
base_model_path = os.path.join(config.BASE_DIR, "modeles", base_model)

# Si le modèle medium n'est pas dispo, utiliser nano
if not os.path.exists(base_model_path):
    # Essayer de le télécharger via ultralytics
    logger.info(f"📥 Modèle {base_model} non trouvé localement, téléchargement...")
    base_model_path = base_model  # Ultralytics téléchargera automatiquement

# Vérifier GPU
import torch
gpu_available = torch.cuda.is_available()
device = "0" if gpu_available else "cpu"

# ============================================================
#  AFFICHAGE DE LA CONFIGURATION
# ============================================================
logger.info("=" * 65)
logger.info("  Smart Parking — Entraînement du Modèle IA v3.0")
logger.info("=" * 65)
logger.info(f"  Modèle de base     : {base_model}")
logger.info(f"  Dataset            : {dataset_name}")
logger.info(f"  data.yaml          : {data_yaml}")
logger.info(f"  Epochs             : {epochs}")
logger.info(f"  Batch size         : {config.TRAINING_BATCH_SIZE}")
logger.info(f"  Taille des images  : {config.TRAINING_IMAGE_SIZE}px")
logger.info(f"  Early stopping     : patience={config.TRAINING_PATIENCE}")
logger.info(f"  Device             : {'🚀 GPU (' + torch.cuda.get_device_name(0) + ')' if gpu_available else '🐢 CPU (lent)'}")
logger.info(f"  Reprise            : {'Oui' if resume else 'Non'}")
logger.info("-" * 65)
logger.info("  Data Augmentation :")
aug = config.TRAINING_AUGMENTATION
logger.info(f"    HSV (h/s/v)      : {aug['hsv_h']}/{aug['hsv_s']}/{aug['hsv_v']}")
logger.info(f"    Mosaïque         : {aug['mosaic']}")
logger.info(f"    Mixup            : {aug['mixup']}")
logger.info(f"    Flip horizontal  : {aug['fliplr']}")
logger.info(f"    Scale            : {aug['scale']}")
logger.info("=" * 65)

if not gpu_available:
    logger.warning("⚠️  ATTENTION : Pas de GPU détecté !")
    logger.warning("    L'entraînement sera TRÈS lent sur CPU.")
    logger.warning("    Durée estimée : 2-12 heures selon le dataset.")
    logger.warning("    Recommandé : utilisez Google Colab avec GPU gratuit.")
    logger.warning("")

    response = input("    Continuer sur CPU ? (o/n) : ").strip().lower()
    if response != 'o':
        logger.info("⏹️  Annulé. Utilisez un GPU pour de meilleurs résultats.")
        sys.exit(0)

# ============================================================
#  ENTRAÎNEMENT
# ============================================================
logger.info("🧠 Chargement du modèle de base...")
model = YOLO(base_model_path)

logger.info("🏋️ Début de l'entraînement — L'IA va étudier votre dataset...")
logger.info("   (Vous pouvez suivre les métriques en temps réel dans le terminal)")
logger.info("")
start_time = datetime.now()

try:
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=config.TRAINING_IMAGE_SIZE,
        batch=config.TRAINING_BATCH_SIZE,
        device=device,
        patience=config.TRAINING_PATIENCE,

        # Data augmentation avancée
        hsv_h=aug["hsv_h"],
        hsv_s=aug["hsv_s"],
        hsv_v=aug["hsv_v"],
        degrees=aug["degrees"],
        translate=aug["translate"],
        scale=aug["scale"],
        shear=aug["shear"],
        flipud=aug["flipud"],
        fliplr=aug["fliplr"],
        mosaic=aug["mosaic"],
        mixup=aug["mixup"],
        copy_paste=aug["copy_paste"],

        # Optimisation
        optimizer="auto",           # AdamW ou SGD (auto-sélection)
        lr0=0.01,                   # Learning rate initial
        lrf=0.01,                   # Learning rate final (ratio)
        warmup_epochs=3,            # Epochs de warmup
        weight_decay=0.0005,        # Régularisation L2
        close_mosaic=10,            # Désactiver mosaïque les 10 derniers epochs

        # Sauvegarde
        plots=True,
        save=True,
        save_period=10,             # Checkpoint tous les 10 epochs
        project=os.path.join(config.BASE_DIR, "runs"),
        name=f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}",

        # Reprise
        resume=resume,

        # Verbosité
        verbose=True,
    )

    duration = datetime.now() - start_time

    # ============================================================
    #  RÉSULTATS ET EXPORT
    # ============================================================
    logger.info("")
    logger.info("=" * 65)
    logger.info("🎉 ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
    logger.info("=" * 65)
    logger.info(f"  Durée totale       : {str(duration).split('.')[0]}")

    # Trouver le meilleur modèle
    best_model_path = None
    runs_dir = os.path.join(config.BASE_DIR, "runs")
    if os.path.exists(runs_dir):
        # Trouver le dossier d'entraînement le plus récent
        training_dirs = sorted(
            [d for d in os.listdir(runs_dir) if d.startswith("training_")],
            reverse=True
        )
        if training_dirs:
            latest = os.path.join(runs_dir, training_dirs[0], "weights", "best.pt")
            if os.path.exists(latest):
                best_model_path = latest

    if best_model_path:
        # Copier best.pt dans modeles/
        dest = config.MODEL_CUSTOM_PATH
        shutil.copy2(best_model_path, dest)
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        logger.info(f"  Meilleur modèle    : {best_model_path}")
        logger.info(f"  Copié vers         : {dest} ({size_mb:.1f} Mo)")
        logger.info("")
        logger.info("  📊 Le modèle best.pt a été automatiquement mis à jour !")
        logger.info("     Redémarrez le serveur IA pour utiliser le nouveau modèle.")
    else:
        logger.warning("  ⚠️ Impossible de trouver best.pt automatiquement")
        logger.info(f"     Cherchez dans : {runs_dir}")
        logger.info(f"     Et copiez best.pt dans : {config.MODEL_CUSTOM_PATH}")

    logger.info("=" * 65)

except KeyboardInterrupt:
    logger.info("\n⏹️  Entraînement interrompu par l'utilisateur.")
    logger.info("   Les checkpoints sauvegardés sont dans le dossier 'runs/'")

except Exception as e:
    logger.error(f"❌ Erreur pendant l'entraînement : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
