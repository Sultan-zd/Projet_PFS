import cv2
import json
import requests
import time # NOUVEAU : Pour gérer le chronomètre
from ultralytics import YOLO

print("Chargement de l'IA...")
model = YOLO('../../modeles/yolov8n.pt')

print("Chargement de la carte des places...")
with open('../../medias/places.json', 'r') as f:
    places = json.load(f)

API_URL = 'http://localhost:8080/api/parking/update'

# --- NOUVEAU : Ouverture du flux vidéo ---
# Remplace 'parking_video.mp4' par 0 si tu veux utiliser ta webcam !
cap = cv2.VideoCapture('../../medias/parking_video1.mp4')

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la vidéo ou la caméra.")
    exit()

# NOUVEAU : On prépare un chronomètre pour ne pas spammer le serveur
dernier_envoi = time.time()
intervalle_envoi = 3.0 # On envoie les données à Spring Boot toutes les 3 secondes

print("Démarrage du flux vidéo en direct... (Appuie sur la touche 'q' pour quitter)")

# NOUVEAU : La boucle infinie qui lit la vidéo image par image
while cap.isOpened():
    ret, frame = cap.read() # ret est un booléen qui dit si l'image a bien été lue
    
    if not ret:
        print("Fin de la vidéo ou coupure du flux.")
        break # Si la vidéo est finie, on sort de la boucle

    # L'IA analyse l'image actuelle (frame)
    results = model(frame)
    voitures_detectees = results[0].boxes

    # On vérifie si c'est le moment d'envoyer les données au serveur
    temps_actuel = time.time()
    faut_il_envoyer = (temps_actuel - dernier_envoi) > intervalle_envoi

    for place in places:
        x1, y1 = place['x'], place['y']
        x2, y2 = x1 + place['largeur'], y1 + place['hauteur']
        
        place_occupee = False

        for boite in voitures_detectees:
            classe_id = int(boite.cls[0])
            if classe_id in [2, 3, 5, 7]: # Véhicules
                vx1, vy1, vx2, vy2 = map(int, boite.xyxy[0])
                centre_x = (vx1 + vx2) // 2
                centre_y = (vy1 + vy2) // 2
                
                if x1 < centre_x < x2 and y1 < centre_y < y2:
                    place_occupee = True
                    break 

        # Si 3 secondes se sont écoulées, on met à jour la base de données
        if faut_il_envoyer:
            donnees = {"numeroPlace": f"P{place['id']}", "occupee": place_occupee}
            try:
                requests.post(API_URL, json=donnees)
            except:
                pass # On ignore l'erreur d'affichage pour ne pas polluer le terminal vidéo

        # Dessiner sur l'image en direct
        if place_occupee:
            couleur = (0, 0, 255) # Rouge
            texte = "Occupee"
        else:
            couleur = (0, 255, 0) # Vert
            texte = "Libre"

        cv2.rectangle(frame, (x1, y1), (x2, y2), couleur, 2)
        cv2.putText(frame, f"P{place['id']}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, couleur, 2)

    # Réinitialiser le chronomètre après un envoi
    if faut_il_envoyer:
        print(f"[{time.strftime('%H:%M:%S')}] -> Base de données mise à jour.")
        dernier_envoi = temps_actuel

    # --- NOUVEAU : Afficher la vidéo en direct dans une fenêtre ---
    cv2.imshow("Smart Parking - Live Video", frame)

    # NOUVEAU : Permet de quitter proprement en appuyant sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Arrêt manuel du système.")
        break

# Libérer les ressources quand c'est fini
cap.release()
cv2.destroyAllWindows()