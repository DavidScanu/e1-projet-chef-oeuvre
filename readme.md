# 🚢⛵🛥️ E1 - Projet chef d'œuvre : Trafic Maritime

Ce projet chef-d'œuvre (réf. E1) témoigne de la maîtrise des compétences visées pour l'obtention du titre professionnel : [Développeur en intelligence artificielle (RNCP 34757)](https://www.francecompetences.fr/recherche/rncp/34757/), délivré par [Simplon](https://simplon.co/), dans le cadre de l'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/). Ce projet chef-d'œuvre implique la création d'un programme d'intelligence artificielle complet, ainsi que le développement d'une application web qui le déploie.

> 🎓 Projet développé par [David Scanu](https://www.linkedin.com/in/davidscanu14/), étudiant en intelligence artificielle 🤖 à l'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/), 1ère promotion de Caen (2023-2024).

## 🛳️ Résumé

Ce projet se concentre sur la détection de bateaux à partir de vues aériennes. L'objectif principal est d'implémenter un modèle de détection d'objets et de suivi d'objets pour identifier et suivre les bateaux dans une scène.

| | |
| --- | --- | 
| Domaine | Vision par ordinateur | 
| Tâches | Détection d'objet et suivi d’instance |


### 🔭 Usages possibles

Voici quelques usages possibles pour l'application de détection et de suivi de bateaux depuis des vues aériennes :

- **Surveillance du trafic maritime** : Déterminer le nombre de passages de bateaux par heure dans un canal ou une zone spécifique, ce qui permet de surveiller l'activité maritime et d'analyser les tendances de trafic.
- **Mesure de la vitesse des bateaux** : Mesurer la vitesse des bateaux en mouvement, offrant ainsi des données précieuses pour la navigation et le contrôle de la vitesse dans certaines zones maritimes.
- **Contrôle de la taille des bateaux** : Surveiller et contrôler les dimensions des bateaux pour s'assurer qu'ils respectent les limites de taille établies dans certaines zones maritimes ou canaux.

## 💻 Application web 

### Fonctionnalités

Cette application web de détection propose **la détection d’objets et le suivi d’instances à partir d'images, de vidéos ou d'URL YouTube**. Ses fonctionnalités principales comprennent :

- **Importation** d'images, de vidéos ou d'URL YouTube.
- **Détection** et suivi d'objets en temps réel grâce à une interface web performante.
- **Annotation** des résultats directement sur le navigateur, avec chaque objet entouré d'une boîte de délimitation.
- **Utilisation simple** : il suffit d'ouvrir l'application dans le navigateur, d'importer le fichier ou d'insérer l'URL YouTube, et de laisser l'application travailler.
- **Exploration des résultats** : Consultation des annotations (labels de classe, coordonnées des boîtes de détection et score de confiance) pour obtenir des informations détaillées sur chaque objet détecté.

### Technologies utilisées

Cette application utilise : 

- Un modèle [Yolov8](https://docs.ultralytics.com/fr) personnalisé pour réaliser les détections dans les images et les vidéos.
- Le framework front-end Python [Streamlit](https://streamlit.io/), reconnu pour sa simplicité, son prototypage rapide et interactif, ainsi que pour son caractère open-source et gratuit.

### Utilisation 

- Sélectionnez la tâche (Détection, Segmentation)
- Sélectionnez la confiance du modèle
- Utilisez le curseur pour ajuster le seuil de confiance (25-100) du modèle.

#### 🖼️ Détection sur une image

- L'image par défaut avec son image d'objets détectés est affichée sur la page principale.
- Sélectionnez une source (sélection du bouton radio Image).
- Téléchargez une image en cliquant sur le bouton "Parcourir les fichiers".
- Cliquez sur le bouton "Détecter les objets" pour exécuter l'algorithme de détection d'objets sur l'image téléchargée avec le seuil de confiance sélectionné.
- L'image résultante avec les objets détectés sera affichée sur la page. Cliquez sur le bouton "Télécharger l'image" pour télécharger l'image. ("Si enregistrer l'image pour télécharger" est sélectionné)

#### 📽️ Détection des vidéos

- Créez un dossier avec le nom « vidéos » dans le même répertoire
- Déposez vos vidéos dans le dossier `videos`
- Dans `settings.py`, éditez les lignes suivantes.

```python
# Vidéos
VIDEO_DIR = ROOT / 'videos'

# Supposons que vous ayez quatre vidéos dans le dossier videos
# Modifiez le nom de la vidéo_1, 2, 3, 4 (avec les noms de vos fichiers vidéo)
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4' 
VIDEO_2_PATH = VIDEO_DIR / 'video_2.mp4'
VIDEO_3_PATH = VIDEO_DIR / 'video_3.mp4'
VIDEO_4_PATH = VIDEO_DIR / 'video_4.mp4'

# Modifiez les mêmes noms ici également.
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
    'video_4': VIDEO_4_PATH,
}

# Vos vidéos commenceront à apparaître dans l'application « Choisir une vidéo ».
```

- Cliquez sur le bouton **Détecter les objets vidéo** et la tâche sélectionnée (détection ou segmentation) démarrera sur la vidéo sélectionnée.

#### 🌊 Détection sur RTSP

- Sélectionnez le bouton **flux RTSP**
- Entrez l'URL RTSP dans la zone de texte et cliquez sur le bouton `Détecter les objets`.

#### 📺 Détection sur l'URL de la vidéo YouTube

- Sélectionnez la source comme **YouTube**.
- Copiez et collez l'URL dans la zone de texte.
- La tâche de détection/segmentation démarrera sur l'url de la vidéo YouTube.

### ❌ Problèmes rencontrés 

| | Titre  | Solution  | URL |
|---|---|---|---|
| 1 | Problème d'importation d'Ultralytics au lancement de Streamlit (`streamlit run app.py`) dans un Codespace GitHub | `apt install libgl1-mesa-glx` | [Lien](https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo) |

## 🤖 Développement du modèle de détection et de suivi `Yolov8`

> **Objectif :** Créer un modèle distillé pour la détection et le suivi de bateaux à partir d'images aériennes non étiquetées.

### 🧪 Processus

1. **Auto-étiquetage des images:**
    - Utiliser le modèle de base [GroundedSAM](https://github.com/IDEA-Research/Grounded-Segment-Anything) avec [Autodistill](https://docs.autodistill.com/) pour annoter automatiquement les images aériennes avec une ontologie définie.
    - L'ontologie définit le type d'objets à détecter (bateaux) et comment le modèle de base est "prompté".

2. **Entraînement du modèle cible:**
    - Utiliser les images annotées automatiquement pour entraîner un modèle cible [Yolov8](https://docs.ultralytics.com/fr).
    - Le modèle cible est optimisé pour la détection précise de bateaux dans les images aériennes.

### 💎 Avantages

- Réduction du temps d'étiquetage manuel des données.
- Prototypage rapide et évaluation de la faisabilité de l'application.
- Modèle distillé précis et performant pour la détection de bateaux.

### 🔑 Points clés

- **Ontologie:** Définit la structure et le contenu des annotations automatiques.
- **Modèle de base:** GroundedSAM avec Autodistill pour l'étiquetage automatique.
- **Modèle cible:** YOLOv8 pour la détection précise de bateaux.

### 📑 Remarques:

- Cette approche est un exemple d'application de la distillation de modèle pour la vision par ordinateur.
- D'autres modèles de base et cibles peuvent être utilisés en fonction des besoins spécifiques.
- L'ontologie est un élément crucial pour la précision et l'efficacité du processus.

### 📓 Notebooks

L'ensemble du processus de développement du modèle est disponible dans les notebooks suivants : 

| Titre  | Notebook  |
|---|---|
| 🏷️ Annotations automatiques avec un modèle de base (Base model) | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Yx053xJrMfcenIW45f8v8zPoFTJsgiMc) |
| 🗃️ Sauvegarde des données d'entraînement dans la base de donnée analytique | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1jA2w1WXoHqTiMBOleNLnS_3WEFtzmI-Q?usp=sharing) |
| 🚂 Entraînement du modèle cible YOLOv8 (Target model) | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1R9Rb8FRNEGeHdfeHdDyOKfAEbkOrSPEB?usp=sharing) |

### 🔗 Ressources supplémentaires

- https://docs.autodistill.com/
- [https://docs.ultralytics.com/fr](https://docs.ultralytics.com/fr)
- [https://github.com/autodistill/autodistill-grounded-sam](https://github.com/autodistill/autodistill-grounded-sam)
- [https://docs.autodistill.com/base_models/groundedsam/](https://docs.autodistill.com/base_models/groundedsam/)
- [https://roboflow.com/train/grounded-sam-and-detr](https://roboflow.com/train/grounded-sam-and-detr)

## 📦 Livrables

- Un **rapport** qui reprend les différentes étapes de conception et de production du projet.
- Une **présentation** du projet, incluant une démonstration.
- Une **application web** fonctionnelle disponible à l’URL : [url]
- Le **code de l’application web** disponible dans ce dépôt GitHub
- Les **notebooks** de conception du modèle de vision par ordinateur
- La **page de gestion de projet** [GitHub Projects](https://github.com/users/DavidScanu/projects/3)

## 📅 Gestion de projet 

[GitHub Project](https://github.com/users/DavidScanu/projects/3) utilisé pour la gestion de ce projet.

## 👀 A propos 

Projet développé par **David Scanu**, étudiant en intelligence artificielle 🤖 à l'**École Microsoft IA par Simplon et ISEN**, 1ère promotion de Caen (2023-2024).

- [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davidscanu14/)
- [![image alt text](https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=dev.to&logoColor=white)](https://dev.to/davidscanu)
- [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://davidscanu.medium.com/)

### 🎓 L’École IA Microsoft par Simplon et ISEN

L'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/) est une formation en **intelligence artificielle** offrant :

- Une certification professionnelle reconnue par l'État (RNCP34757)
- Une certification Agile
- Deux certifications Microsoft Azure.

En 2018, Microsoft a créé cette école en partenariat avec Simplon, un réseau de fabriques numériques, pour offrir des opportunités d'emploi dans le domaine de l'IA.  La formation comprend l'apprentissage des bases du développement, la maîtrise des données et la conception et le développement de modèles prédictifs de Machine Learning et de Deep Learning.

Cette formation s’effectue en deux temps: après avoir suivi une formation intensive de 7 mois, nous sommes entrés en contrat de professionnalisation de 14 mois en alternance au sein d’une entreprise locale.