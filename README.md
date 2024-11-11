# Test_Technique_MyTeam_AI
Voici un exemple de fichier README pour expliquer comment exécuter le code :

---

# Object Detection with Tkinter and MediaPipe

Ce projet permet de capturer une vidéo en temps réel depuis votre caméra et d'effectuer une détection d'objets à l'aide de l'API **MediaPipe**. Il utilise un modèle **EfficientDet** pour détecter des objets et affiche les résultats avec des boîtes de délimitation dans une interface graphique construite avec **Tkinter**.


## Prérequis

Avant d'exécuter le script, vous devez avoir installé **Python** et créer un environnement virtuel pour gérer les dépendances. Ce projet nécessite les bibliothèques suivantes :
- **opencv-python** pour la capture vidéo.
- **mediapipe** pour la détection d'objets.
- **pillow** pour l'intégration avec Tkinter.
- **requests** pour télécharger le modèle de détection si nécessaire.

### Installation des prérequis

1. **Installer Python**  
   Assurez-vous d'avoir **Python 3.x** installé sur votre machine. Vous pouvez vérifier en exécutant la commande suivante dans votre terminal :
   ```bash
   python --version
   ```

2. **Créer un environnement virtuel**  
   Dans le terminal, naviguez vers le dossier où vous souhaitez créer le projet et exécutez les commandes suivantes :

   ```bash
   python -m venv myenv
   ```

3. **Activer l'environnement virtuel**  
   - **Sous Windows :**
     ```bash
     .\myenv\Scripts\activate
     ```
   - **Sous macOS/Linux :**
     ```bash
     source myenv/bin/activate
     ```

4. **Installer les dépendances**  
   Une fois l'environnement virtuel activé, installez les bibliothèques nécessaires en exécutant :
   ```bash
   pip install opencv-python mediapipe pillow requests
   ```

## Exécution du code

1. **Télécharger le modèle**  
   Le script va automatiquement télécharger le modèle `efficientdet.tflite` à partir de l'URL fournie, si le fichier n'est pas déjà présent dans le répertoire du projet. 

2. **Lancer le script**  
   Exécutez le script Python en utilisant la commande suivante dans votre terminal :
   ```bash
   python Detect_object_adhoc.py
   ```

3. **Contrôler la vidéo**  
   Dans l'interface graphique, vous avez trois boutons :
   - **Start Video** : Démarre la capture vidéo et la détection d'objets.
   - **Stop Video** : Arrête la capture vidéo.
   -** Quit**: Quitte la fenetre apres arret de la video

## Fonctionnement du code

- Le modèle `EfficientDet` est téléchargé (si nécessaire) et chargé pour être utilisé dans le script.
- La caméra est activée pour capturer la vidéo en direct.
- Le modèle effectue une détection d'objets sur chaque frame de la vidéo capturée et affiche les résultats dans l'interface graphique.
- La fenêtre de l'application est redimensionnée pour occuper toute la taille de l'écran.



