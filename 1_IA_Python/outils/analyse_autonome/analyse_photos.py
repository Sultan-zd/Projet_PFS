import cv2
import requests
import os
from ultralytics import YOLO

# Paramètres d'affichage
LARGEUR_ECRAN = 1280
HAUTEUR_ECRAN = 720

print("Chargement du cerveau IA sur-mesure...")
# Vérifie bien que le chemin vers ton best.pt est le bon
model = YOLO('../../modeles/best.pt') 

API_URL = 'http://localhost:8080/api/parking/update'
dossier_photos = '../../medias/photos_parking'

# 1. Sécurité : Vérifier si le dossier existe
if not os.path.exists(dossier_photos):
    print(f"\n❌ ERREUR : Le dossier '{dossier_photos}' n'existe pas !")
    print("Crée-le et mets tes images (.jpg ou .png) à l'intérieur.")
    exit()

# 2. Récupérer la liste de toutes les images dans le dossier
fichiers_images = [f for f in os.listdir(dossier_photos) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if len(fichiers_images) == 0:
    print(f"\n❌ ERREUR : Le dossier '{dossier_photos}' est vide !")
    exit()

# Préparation de la fenêtre
nom_fenetre_final = "Smart Parking - Analyse de Photos"
cv2.namedWindow(nom_fenetre_final, cv2.WINDOW_NORMAL) 
cv2.resizeWindow(nom_fenetre_final, LARGEUR_ECRAN, HAUTEUR_ECRAN)

print(f"\nDémarrage de l'analyse sur {len(fichiers_images)} photos...")
print("👉 INSTRUCTION : Appuie sur N'IMPORTE QUELLE TOUCHE pour passer à la photo suivante.")
print("👉 Appuie sur 'q' pour quitter le programme.")
print("-" * 50)

# 3. Boucle sur chaque image du dossier
for nom_fichier in fichiers_images:
    chemin_complet = os.path.join(dossier_photos, nom_fichier)
    
    # Lecture de l'image (au lieu de cap.read())
    frame_full_hd = cv2.imread(chemin_complet)

    if frame_full_hd is None:
        print(f"⚠️ Impossible de lire le fichier {nom_fichier}, passage au suivant...")
        continue

    print(f"Analyse en cours : {nom_fichier}...")

    # L'IA analyse l'image
    results = model(frame_full_hd, conf=0.60, iou=0.45)
    boites_detectees = results[0].boxes

    places_libres = 0
    places_occupees = 0
    compteur_id = 1

    # Traitement des résultats
    for boite in boites_detectees:
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

        # Envoi IMMÉDIAT à Spring Boot pour chaque photo
        donnees = {"numeroPlace": f"P{compteur_id}", "occupee": place_occupee}
        try:
            requests.post(API_URL, json=donnees, timeout=1.0)
        except requests.exceptions.RequestException:
            pass
        
        # Dessin sur l'image
        cv2.rectangle(frame_full_hd, (x1_full, y1_full), (x2_full, y2_full), couleur, 2)
        cv2.putText(frame_full_hd, f"P{compteur_id}: {texte}", (x1_full, y1_full - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, couleur, 2)
        
        compteur_id += 1

    print(f"Résultat : {places_libres} Libres | {places_occupees} Occupées.")

    # Affichage
    frame_pour_affichage = cv2.resize(frame_full_hd, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
    cv2.imshow(nom_fenetre_final, frame_pour_affichage)

    # 4. Le système de pause
    # cv2.waitKey(0) fige le programme jusqu'à ce que tu appuies sur une touche clavier
    touche = cv2.waitKey(0) & 0xFF
    
    if touche == ord('q'):
        print("\nArrêt manuel demandé.")
        break

cv2.destroyAllWindows()
print("\n✅ Toutes les photos ont été analysées !")