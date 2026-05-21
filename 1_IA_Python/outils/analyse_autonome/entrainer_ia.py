from ultralytics import YOLO

print("1. Chargement du modèle de base (le cerveau vierge)...")
# On utilise yolov8n.pt car c'est le plus rapide et le plus léger pour commencer
model = YOLO('../../modeles/yolov8n.pt') 

print("2. Début de l'entraînement ! L'IA va étudier ton dataset...")
# --- PARAMÈTRES D'ENTRAÎNEMENT ---
# data : Le chemin vers le fichier de configuration de ton dataset
# epochs : Le nombre de cycles d'apprentissage (50 est un bon test)
# imgsz : La taille des images
# plots=True : Demande à YOLO de dessiner des graphiques de ses performances

try:
    results = model.train(
        data='../../medias/dataset_parking/data.yaml', 
        epochs=5, 
        imgsz=640,
        plots=True
    )
    print("\n🎉 Entraînement terminé avec succès ! Ton nouveau cerveau est prêt.")
except Exception as e:
    print(f"\n❌ Erreur pendant l'entraînement : {e}")