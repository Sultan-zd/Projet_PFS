import cv2
import json
import numpy as np

nom_video = '../../medias/parking_video.mp4'
fichier_json = '../../medias/places.json'

LARGEUR_ECRAN = 1280
HAUTEUR_ECRAN = 720

# Liste pour stocker les places
places = []
points_actuels = []
compteur_place = 1

def dessiner_polygone(event, x, y, flags, param):
    global points_actuels, compteur_place, frame_copie

    if event == cv2.EVENT_LBUTTONDOWN:
        # Ajoute le point cliqué
        points_actuels.append([x, y])
        cv2.circle(frame_copie, (x, y), 5, (0, 0, 255), -1)
        
        # Si on a cliqué 4 points, on ferme le polygone (la place de parking)
        if len(points_actuels) == 4:
            pts = np.array(points_actuels, np.int32)
            cv2.polylines(frame_copie, [pts], True, (0, 255, 0), 2)
            cv2.putText(frame_copie, f"P{compteur_place}", (points_actuels[0][0], points_actuels[0][1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # On enregistre la place
            places.append({
                "id": f"P{compteur_place}",
                "points": points_actuels.copy() # C'est ici que la clé 'points' est créée !
            })
            
            print(f"✅ Place P{compteur_place} enregistrée !")
            compteur_place += 1
            points_actuels = [] # On réinitialise pour la place suivante

        cv2.imshow("Configuration des places", frame_copie)

# Lire la première image de la vidéo
cap = cv2.VideoCapture(nom_video)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Erreur : Impossible de lire la vidéo.")
    exit()

# Redimensionner l'image pour l'écran
frame = cv2.resize(frame, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
frame_copie = frame.copy()

cv2.namedWindow("Configuration des places")
cv2.setMouseCallback("Configuration des places", dessiner_polygone)

print("=====================================================")
print("🛠️ OUTIL DE CONFIGURATION DES PLACES (NOUVELLE VERSION)")
print("=====================================================")
print("Pour CHAQUE place : Clique sur les 4 coins (en tournant dans le même sens).")
print("Appuie sur 's' pour SAUVEGARDER et quitter.")
print("Appuie sur 'q' pour QUITTER SANS SAUVEGARDER.")
print("=====================================================")

cv2.imshow("Configuration des places", frame_copie)

while True:
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('s'):
        # Sauvegarder dans le fichier JSON
        with open(fichier_json, 'w') as f:
            json.dump(places, f, indent=4)
        print(f"\n💾 SUCCÈS : {len(places)} places sauvegardées dans '{fichier_json}'.")
        break
    elif key == ord('q'):
        print("\nAnnulation. Aucune sauvegarde effectuée.")
        break

cv2.destroyAllWindows()