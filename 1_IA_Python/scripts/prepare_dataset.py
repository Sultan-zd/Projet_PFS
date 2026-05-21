"""
============================================================
 Smart Parking — Préparation du Dataset PKLot pour Entraînement
============================================================
 Ce script télécharge et prépare le dataset PKLot (Parking Lot)
 depuis Roboflow Universe pour entraîner un modèle YOLOv8
 performant capable de détecter les places vides et occupées
 dans n'importe quel parking.

 Le dataset PKLot contient des images de 3 parkings différents
 sous différentes conditions météorologiques (soleil, pluie,
 couvert), ce qui le rend idéal pour la généralisation.

 Usage : python prepare_dataset.py
============================================================
"""

import os
import sys
import json
import shutil
import logging
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("PrepareDataset")


def prepare_pklot_with_roboflow():
    """
    Télécharge le dataset PKLot via l'API Roboflow.
    Nécessite : pip install roboflow
    """
    try:
        from roboflow import Roboflow
    except ImportError:
        logger.error("❌ La bibliothèque 'roboflow' n'est pas installée.")
        logger.info("   Installez-la avec : pip install roboflow")
        return False

    target_dir = config.PKLOT_DATASET_DIR
    os.makedirs(target_dir, exist_ok=True)

    logger.info("=" * 60)
    logger.info("  Téléchargement du Dataset PKLot via Roboflow")
    logger.info("=" * 60)
    logger.info(f"  Destination : {target_dir}")
    logger.info("=" * 60)

    try:
        # PKLot sur Roboflow Universe (version publique)
        # Vous pouvez aussi utiliser votre propre clé API
        rf = Roboflow(api_key="YOUR_API_KEY")  # Remplacez par votre clé
        project = rf.workspace().project("pklot-detect")
        version = project.version(1)
        dataset = version.download("yolov8", location=target_dir)

        logger.info(f"✅ Dataset PKLot téléchargé dans {target_dir}")
        return True

    except Exception as e:
        logger.warning(f"⚠️ Erreur Roboflow : {e}")
        logger.info("   Utilisation du dataset existant à la place...")
        return False


def merge_datasets(existing_dir: str, pklot_dir: str, output_dir: str):
    """
    Fusionne le dataset existant (Roboflow du user) avec le dataset PKLot
    pour créer un super-dataset combiné.
    """
    logger.info("🔄 Fusion des datasets...")

    os.makedirs(output_dir, exist_ok=True)

    total_images = 0

    for split in ["train", "valid", "test"]:
        img_out = os.path.join(output_dir, split, "images")
        lbl_out = os.path.join(output_dir, split, "labels")
        os.makedirs(img_out, exist_ok=True)
        os.makedirs(lbl_out, exist_ok=True)

        # Copier depuis le dataset existant
        for source_dir in [existing_dir, pklot_dir]:
            src_img = os.path.join(source_dir, split, "images")
            src_lbl = os.path.join(source_dir, split, "labels")

            if os.path.exists(src_img):
                for f in os.listdir(src_img):
                    src = os.path.join(src_img, f)
                    dst = os.path.join(img_out, f)
                    if not os.path.exists(dst):
                        shutil.copy2(src, dst)
                        total_images += 1

            if os.path.exists(src_lbl):
                for f in os.listdir(src_lbl):
                    src = os.path.join(src_lbl, f)
                    dst = os.path.join(lbl_out, f)
                    if not os.path.exists(dst):
                        shutil.copy2(src, dst)

    logger.info(f"✅ {total_images} images fusionnées au total")
    return total_images


def create_data_yaml(output_dir: str, class_names: list = None):
    """
    Crée le fichier data.yaml nécessaire pour l'entraînement YOLOv8.
    """
    if class_names is None:
        class_names = ["empty", "occupied"]

    data = {
        "train": os.path.join(output_dir, "train", "images"),
        "val": os.path.join(output_dir, "valid", "images"),
        "test": os.path.join(output_dir, "test", "images"),
        "nc": len(class_names),
        "names": class_names,
    }

    yaml_path = os.path.join(output_dir, "data.yaml")

    # Écrire en format YAML simple
    with open(yaml_path, "w") as f:
        f.write(f"train: {data['train']}\n")
        f.write(f"val: {data['val']}\n")
        f.write(f"test: {data['test']}\n")
        f.write(f"\nnc: {data['nc']}\n")
        f.write(f"names: {data['names']}\n")

    logger.info(f"📄 data.yaml créé : {yaml_path}")
    return yaml_path


def analyze_dataset(dataset_dir: str):
    """
    Analyse le dataset et affiche des statistiques détaillées.
    """
    logger.info("\n📊 Analyse du dataset...")
    logger.info("-" * 40)

    total_images = 0
    total_labels = 0
    class_counts = {}

    for split in ["train", "valid", "test"]:
        img_dir = os.path.join(dataset_dir, split, "images")
        lbl_dir = os.path.join(dataset_dir, split, "labels")

        img_count = 0
        lbl_count = 0

        if os.path.exists(img_dir):
            img_count = len([f for f in os.listdir(img_dir)
                           if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

        if os.path.exists(lbl_dir):
            for f in os.listdir(lbl_dir):
                if f.endswith('.txt'):
                    lbl_count += 1
                    filepath = os.path.join(lbl_dir, f)
                    with open(filepath, 'r') as label_file:
                        for line in label_file:
                            parts = line.strip().split()
                            if parts:
                                cls = int(parts[0])
                                class_counts[cls] = class_counts.get(cls, 0) + 1

        total_images += img_count
        total_labels += lbl_count
        logger.info(f"  {split:6s} : {img_count:5d} images, {lbl_count:5d} labels")

    logger.info("-" * 40)
    logger.info(f"  TOTAL  : {total_images:5d} images, {total_labels:5d} labels")

    if class_counts:
        logger.info("\n  Distribution des classes :")
        names = {0: "empty", 1: "occupied"}
        for cls_id, count in sorted(class_counts.items()):
            name = names.get(cls_id, f"class_{cls_id}")
            logger.info(f"    [{cls_id}] {name:12s} : {count:6d} annotations")

    return total_images


def prepare_existing_dataset():
    """
    Vérifie et prépare le dataset existant du user (Roboflow).
    S'assure que tout est en ordre pour l'entraînement.
    """
    dataset_dir = config.DATASET_DIR

    if not os.path.exists(dataset_dir):
        logger.error(f"❌ Dataset non trouvé : {dataset_dir}")
        return False

    # Vérifier data.yaml
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    if not os.path.exists(yaml_path):
        logger.warning("⚠️ data.yaml manquant, création automatique...")
        create_data_yaml(dataset_dir)

    # Analyser le dataset
    total = analyze_dataset(dataset_dir)

    if total == 0:
        logger.error("❌ Aucune image trouvée dans le dataset")
        return False

    logger.info(f"\n✅ Dataset existant prêt avec {total} images")
    return True


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("  Smart Parking — Préparation du Dataset")
    logger.info("=" * 60)

    # Étape 1 : Vérifier le dataset existant
    logger.info("\n📂 Étape 1 : Vérification du dataset existant...")
    existing_ok = prepare_existing_dataset()

    # Étape 2 : Essayer de télécharger PKLot
    logger.info("\n📥 Étape 2 : Tentative de téléchargement PKLot...")
    pklot_ok = False

    if "--download-pklot" in sys.argv:
        pklot_ok = prepare_pklot_with_roboflow()
    else:
        logger.info("   Skipping PKLot download (utilisez --download-pklot pour activer)")
        logger.info("   Vous pouvez aussi télécharger manuellement depuis :")
        logger.info("   https://universe.roboflow.com/search?q=pklot")
        logger.info("   Et placer les fichiers dans medias/pklot_dataset/")

    # Étape 3 : Fusion si PKLot disponible
    if pklot_ok and existing_ok:
        merged_dir = os.path.join(config.MEDIA_DIR, "merged_dataset")
        logger.info(f"\n🔄 Étape 3 : Fusion des datasets dans {merged_dir}...")
        merge_datasets(config.DATASET_DIR, config.PKLOT_DATASET_DIR, merged_dir)
        create_data_yaml(merged_dir)
        analyze_dataset(merged_dir)
        logger.info(f"\n🎉 Dataset fusionné prêt ! Utilisez ce chemin pour l'entraînement :")
        logger.info(f"   {os.path.join(merged_dir, 'data.yaml')}")
    elif existing_ok:
        logger.info("\n✅ Dataset existant sera utilisé pour l'entraînement")
        logger.info(f"   {config.TRAINING_DATA_YAML}")
    else:
        logger.error("\n❌ Aucun dataset disponible pour l'entraînement")

    logger.info("\n" + "=" * 60)
    logger.info("  Prochaine étape : python entrainer_ia.py")
    logger.info("=" * 60)
