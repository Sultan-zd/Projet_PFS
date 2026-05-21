import cv2
import requests
import time
import os
import json
import numpy as np
from ultralytics import YOLO

# --- Paramètres d'ingénieur ---
LARGEUR_ECRAN = 1280
HAUTEUR_ECRAN = 720
DELAI_CONFIRMATION_LIBRE = 10  # Secondes avant de confirmer qu'une place est libre
# ------------------------------

print("Chargement du Cerveau IA COCO (yolov8n)...")
model = YOLO('../../modeles/yolov8n.pt') 

API_URL = 'http://localhost:8080/api/parking/update'
nom_video = '../../medias/parking_video.mp4'
fichier_places = '../../medias/places.json'

with open(fichier_places, 'r') as f:
    places_definies = json.load(f)

# --- NOUVEAU : Dictionnaire pour suivre le temps d'occupation ---
# Clé : ID de la place, Valeur : Timestamp de la dernière détection "Occupée"
derniers_moments_occupes = {}

cap = cv2.VideoCapture(nom_video)
dernier_envoi = time.time()
intervalle_envoi = 3.0

while True:
    ret, frame_full_hd = cap.read()
    if not ret: break

    frame = cv2.resize(frame_full_hd, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
    results = model(frame, conf=0.25)
    boites_detectees = results[0].boxes

    temps_actuel = time.time()
    faut_il_envoyer = (temps_actuel - dernier_envoi) > intervalle_envoi

    for place in places_definies:
        id_place = place['id']
        points_place = np.array(place['points'], np.int32)
        
        # 1. On vérifie si l'IA voit une voiture à cet instant T
        voiture_detectee_maintenant = False
        for boite in boites_detectees:
            classe_id = int(boite.cls[0])
            nom_classe = model.names[classe_id].lower() 
            
            if nom_classe in ['car', 'truck', 'bus']:
                x1, y1, x2, y2 = map(int, boite.xyxy[0])
                cx = int((x1 + x2) / 2)
                # Test multi-points pour la précision
                points_test = [int((y1 + y2) / 2), int(y2 - 5), int(y1 + 0.75 * (y2 - y1))]
                
                if any(cv2.pointPolygonTest(points_place, (cx, p), False) >= 0 for p in points_test):
                    voiture_detectee_maintenant = True
                    break

        # 2. LOGIQUE DE TEMPORISATION (Anti-Flickering)
        if voiture_detectee_maintenant:
            # Si on voit une voiture, on met à jour l'heure de dernière occupation
            derniers_moments_occupes[id_place] = temps_actuel
            place_occupee_finale = True
        else:
            # Si on ne voit plus de voiture, on vérifie depuis combien de temps
            dernier_vu_occupe = derniers_moments_occupes.get(id_place, 0)
            temps_ecoule = temps_actuel - dernier_vu_occupe
            
            if temps_ecoule < DELAI_CONFIRMATION_LIBRE:
                # Moins de 10s : on considère qu'elle est TOUJOURS occupée (sécurité)
                place_occupee_finale = True
            else:
                # Plus de 10s : on confirme enfin qu'elle est libre
                place_occupee_finale = False

        # 3. Affichage et Envoi
        couleur = (0, 0, 255) if place_occupee_finale else (0, 255, 0)
        etat_texte = "Occupee" if place_occupee_finale else "Libre"

        if faut_il_envoyer:
            try:
                requests.post(API_URL, json={"numeroPlace": id_place, "occupee": place_occupee_finale}, timeout=1.0)
            except requests.exceptions.RequestException:
                pass

        cv2.polylines(frame, [points_place], True, couleur, 2)
        cv2.putText(frame, f"{id_place}: {etat_texte}", (points_place[0][0], points_place[0][1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, couleur, 2)

    if faut_il_envoyer: dernier_envoi = temps_actuel
    cv2.imshow("Smart Parking - Temporisation 10s", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()