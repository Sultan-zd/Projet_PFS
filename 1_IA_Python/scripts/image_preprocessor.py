"""
============================================================
 Smart Parking Analysis — Prétraitement d'Image Intelligent
============================================================
 Module de prétraitement automatique qui améliore la qualité
 des images avant l'analyse IA. Adapte le traitement en
 fonction des conditions de luminosité détectées.

 Techniques utilisées :
   - CLAHE  : Amélioration adaptative du contraste
   - Gamma  : Correction de luminosité
   - Denoise: Réduction du bruit (filtre bilatéral)
============================================================
"""

import cv2
import numpy as np
import logging

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

logger = logging.getLogger("ImagePreprocessor")


class ImagePreprocessor:
    """
    Préprocesseur d'images intelligent pour l'analyse de parking.
    Détecte automatiquement les conditions de luminosité et applique
    les corrections appropriées.
    """

    def __init__(self):
        """Initialise le préprocesseur avec les paramètres de config."""
        self.clahe = cv2.createCLAHE(
            clipLimit=config.CLAHE_CLIP_LIMIT,
            tileGridSize=config.CLAHE_TILE_SIZE
        )
        self._stats = {"processed": 0, "dark_corrected": 0, "bright_corrected": 0}
        logger.info("🖼️  Préprocesseur d'images initialisé")

    def process(self, frame: np.ndarray) -> np.ndarray:
        """
        Pipeline de prétraitement complet.

        Args:
            frame: Image BGR (numpy array)

        Returns:
            Image prétraitée (BGR)
        """
        if not config.ENABLE_PREPROCESSING:
            return frame

        result = frame.copy()

        # 1. Analyser la luminosité
        brightness = self._get_brightness(result)

        # 2. Correction gamma adaptative
        result = self._apply_gamma_correction(result, brightness)

        # 3. CLAHE (amélioration du contraste)
        result = self._apply_clahe(result)

        # 4. Réduction du bruit (optionnel)
        if config.ENABLE_DENOISING:
            result = self._apply_denoising(result)

        self._stats["processed"] += 1
        return result

    def _get_brightness(self, frame: np.ndarray) -> float:
        """Calcule la luminosité moyenne de l'image."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return float(np.mean(gray))

    def _apply_gamma_correction(self, frame: np.ndarray, brightness: float) -> np.ndarray:
        """
        Applique une correction gamma adaptative.
        - Image trop sombre → éclaircir (gamma > 1)
        - Image trop claire → assombrir (gamma < 1)
        """
        if brightness < config.BRIGHTNESS_LOW_THRESHOLD:
            gamma = config.GAMMA_DARK
            self._stats["dark_corrected"] += 1
        elif brightness > config.BRIGHTNESS_HIGH_THRESHOLD:
            gamma = config.GAMMA_BRIGHT
            self._stats["bright_corrected"] += 1
        else:
            return frame  # Luminosité OK, pas de correction

        # Table de lookup gamma
        inv_gamma = 1.0 / gamma
        table = np.array([
            ((i / 255.0) ** inv_gamma) * 255
            for i in range(256)
        ]).astype("uint8")

        return cv2.LUT(frame, table)

    def _apply_clahe(self, frame: np.ndarray) -> np.ndarray:
        """
        Applique CLAHE (Contrast Limited Adaptive Histogram Equalization).
        Améliore le contraste local sans sur-amplifier le bruit.
        Travaille dans l'espace LAB pour préserver les couleurs.
        """
        # Convertir en LAB
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)

        # Appliquer CLAHE uniquement sur le canal L (luminosité)
        l_enhanced = self.clahe.apply(l_channel)

        # Recombiner
        enhanced = cv2.merge([l_enhanced, a_channel, b_channel])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    def _apply_denoising(self, frame: np.ndarray) -> np.ndarray:
        """
        Applique un filtre bilatéral pour réduire le bruit
        tout en préservant les contours (important pour les voitures).
        """
        return cv2.bilateralFilter(
            frame,
            d=config.DENOISE_STRENGTH,
            sigmaColor=75,
            sigmaSpace=75
        )

    def get_stats(self) -> dict:
        """Retourne les statistiques de prétraitement."""
        return self._stats.copy()
