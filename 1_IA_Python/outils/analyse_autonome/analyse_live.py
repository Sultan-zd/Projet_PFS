import cv2
import requests
import time
import os
from ultralytics import YOLO

# --- NOUVEAU : Paramètre d'ingénieur pour l'affichage ---
# La taille que tu veux pour le fenêtre vidéo qui s'affiche
LARGEUR_ECRAN = 1280
HAUTEUR_ECRAN = 720
# -------------------------------------------------------

print("Chargement du NOUVEAU cerveau IA sur-mesure...")
model = YOLO('../../modeles/best.pt') 

API_URL = 'http://localhost:8080/api/parking/update'
nom_video = '../../medias/parking_video1.mp4'

if not os.path.exists(nom_video):
    print(f"\n❌ ERREUR : Je ne trouve pas le fichier '{nom_video}' !")
    exit()

cap = cv2.VideoCapture(nom_video)

if not cap.isOpened():
    print(f"\n❌ ERREUR : Le fichier '{nom_video}' est là, mais OpenCV n'arrive pas à le lire.")
    exit()

dernier_envoi = time.time()
intervalle_envoi = 3.0

# --- NOUVEAU : On crée la fenêtre d'affichage final ---
nom_fenetre_final = "Smart Parking - IA Autonome"
cv2.namedWindow(nom_fenetre_final, cv2.WINDOW_NORMAL) 
cv2.resizeWindow(nom_fenetre_final, LARGEUR_ECRAN, HAUTEUR_ECRAN)

print(f"Démarrage de l'analyse autonome en direct sur {nom_video}... (Appuie sur 'q' pour quitter)")

while True:
    ret, frame_full_hd = cap.read()
    if not ret:
        print("\nFin de la vidéo atteinte.")
        break

    # 1. L'IA analyse l'image FULL HD
    results = model(frame_full_hd)
    boites_detectees = results[0].boxes

    places_libres = 0
    places_occupees = 0

    temps_actuel = time.time()
    faut_il_envoyer = (temps_actuel - dernier_envoi) > intervalle_envoi

    compteur_id = 1

    # 2. Lecture des résultats sur l'image FULL HD
    for boite in boites_detectees:
        # Coordonnées FULL HD de la place détectée
        x1_full, y1_full, x2_full, y2_full = map(int, boite.xyxy[0])
        
        classe_id = int(boite.cls[0])
        nom_classe = model.names[classe_id].lower() 

        place_occupee = False
        if nom_classe == 'occupied': 
            place_occupee = True
            places_occupees += 1
            couleur = (0, 0, 255) # Rouge
            texte = "Occupee"
        else:
            places_libres += 1
            couleur = (0, 255, 0) # Vert
            texte = "Libre"

        # 3. Envoi à Spring Boot (on envoie toujours l'ID mathématique réel)
        if faut_il_envoyer:
            donnees = {"numeroPlace": f"P{compteur_id}", "occupee": place_occupee}
            try:
                requests.post(API_URL, json=donnees, timeout=1.0)
            except requests.exceptions.RequestException:
                pass
        
        # 4. Dessin sur l'image FULL HD
        cv2.rectangle(frame_full_hd, (x1_full, y1_full), (x2_full, y2_full), couleur, 2)
        cv2.putText(frame_full_hd, f"P{compteur_id}: {texte}", (x1_full, y1_full - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, couleur, 2)
        
        compteur_id += 1

    if faut_il_envoyer:
        print(f"[{time.strftime('%H:%M:%S')}] -> {places_libres} Libres | {places_occupees} Occupées.")
        dernier_envoi = temps_actuel

    # --- NOUVEAU : Transformation mathématique pour l'affichage ---
    # 5. On crée une COPIE de l'image (frame) déjà traitée et dessinée,
    # pour l'affichage final, qui est réduite pour tenir sur l'écran.
    frame_pour_affichage = cv2.resize(frame_full_hd, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

    # Affichage final sur l'image RÉDUITE
    cv2.imshow(nom_fenetre_final, frame_pour_affichage)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Arrêt manuel.")
        break

cap.release()
cv2.destroyAllWindows()