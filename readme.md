# 🚢⛵🛥️ E1 - Projet chef d'œuvre : Trafic Maritime

Ce projet chef-d'œuvre témoigne de la maîtrise des compétences visées pour l'obtention du titre professionnel : [Développeur en intelligence artificielle (RNCP 34757)](https://www.francecompetences.fr/recherche/rncp/34757/), délivré par [Simplon](https://simplon.co/), dans le cadre de l'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/). Ce projet chef d'œuvre comprend la conception d'un programme d'intelligence artificielle complet et la réalisation d’une application qui met à disposition ce programme.

## Résumé

Mon projet se concentre sur la **détection de bateaux à partir de vues aériennes**. L'objectif principal est d'implémenter des algorithmes de détection d'objets et de suivi d'objets pour identifier et suivre les bateaux dans une scène. Une application potentielle de ce système serait la mesure du nombre de passages de bateaux par heure dans un canal ou une zone spécifique, fournissant ainsi des informations utiles pour la gestion du trafic maritime.

- **Domaine** : Vision par ordinateur
- **Tâche** : Détection d'objets / d’instance, suivi d'objet 

### Usages possibles

- Nombre de passages de bateaux par heure dans un canal ou une zone donnée
- Mesurer la vitesse d'un bateau
- Contrôle de la taille des bateaux, limite de taille

## Livrables

- La **réalisation d'un projet chef d'œuvre**.
- Un **rapport** qui reprend les différentes étapes de conception et de production du projet.
- Une **présentation** du projet, incluant une démonstration.

## Application web

L'objectif de ce projet est la conception d'une **application web**, permettant aux utilisateurs d'importer une image ou une vidéo. L'application réalise la détection d'objets sur le fichier fourni et retourne le résultat annoté, accompagné de :

- les boîtes de délimitation entourant les objets détectés
- les étiquettes de classe
- les scores de confiance associés.

<img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" alt="Streamlit logo" style="margin-top:20px"></img>

L'application est développée à l'aide du framework front-end python : [Streamlit](https://streamlit.io/). Les avantages de Streamlit sont :

- Simple et tout en python
- Prototypage rapide et interactif
- Rafraîchissement automatique
- Open-source et gratuit

## Développement du modèle de détection et de suivi

> **Objectif :** Créer un modèle distillé pour la détection et le suivi de bateaux à partir d'images aériennes non étiquetées.

### Processus

1. **Auto-étiquetage des images:**
    - Utiliser le modèle de base [GroundedSAM](https://github.com/IDEA-Research/Grounded-Segment-Anything) avec [Autodistill](https://docs.autodistill.com/) pour annoter automatiquement les images aériennes avec une ontologie définie.
    - L'ontologie définit le type d'objets à détecter (bateaux) et comment le modèle de base est "prompté".

2. **Entraînement du modèle cible:**
    - Utiliser les images annotées automatiquement pour entraîner un modèle cible [Yolov8](https://docs.ultralytics.com/fr).
    - Le modèle cible est optimisé pour la détection précise de bateaux dans les images aériennes.

### Avantages

- Réduction du temps d'étiquetage manuel des données.
- Prototypage rapide et évaluation de la faisabilité de l'application.
- Modèle distillé précis et performant pour la détection de bateaux.

### Points clés

- **Ontologie:** Définit la structure et le contenu des annotations automatiques.
- **Modèle de base:** GroundedSAM avec Autodistill pour l'étiquetage automatique.
- **Modèle cible:** YOLOv8 pour la détection précise de bateaux.

### Ressources supplémentaires

- [https://github.com/autodistill/autodistill-grounded-sam](https://github.com/autodistill/autodistill-grounded-sam)
- [https://docs.autodistill.com/base_models/groundedsam/](https://docs.autodistill.com/base_models/groundedsam/)
- [https://docs.ultralytics.com/fr](https://docs.ultralytics.com/fr)
- [https://roboflow.com/train/grounded-sam-and-detr](https://roboflow.com/train/grounded-sam-and-detr)

### Remarques:

- Cette approche est un exemple d'application de la distillation de modèle pour la vision par ordinateur.
- D'autres modèles de base et cibles peuvent être utilisés en fonction des besoins spécifiques.
- L'ontologie est un élément crucial pour la précision et l'efficacité du processus.

### Notebooks

L'ensemble du processus de développement du modèle est disponible dans les notebooks suivants : 

| Titre  | Notebook  |
|---|---|
| 🏷️ Annotations automatiques avec un modèle de base (Base model) | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Yx053xJrMfcenIW45f8v8zPoFTJsgiMc) |
| 🗃️ Sauvegarde des données d'entraînement dans la base de donnée analytique | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ZP6E8BIO1QXTTzsHtAj1kscZCsqVs0RL?usp=sharing) |
| 🚂 Entraînement du modèle cible YOLOv8 (Target model) | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ZP6E8BIO1QXTTzsHtAj1kscZCsqVs0RL?usp=sharing) |

## Développement de l'application web

Développement d'une application wbe avec le framework [Streamlit](https://streamlit.io/). Application qui réalise les détections et suivis d'objets à partir d'images, de vidéos ou d'URL YouTube. 

### Problèmes rencontrés 

| | Titre  | Solution  | URL |
|---|---|---|---|
| 1 | Problème d'importation d'Ultralytics au lancement de Streamlit (`streamlit run app.py`) dans un Codespace GitHub | `apt install libgl1-mesa-glx` | [Lien](https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo) |

## Gestion de projet 

[GitHub Project](https://github.com/users/DavidScanu/projects/3) utilisé pour la gestion de ce projet.

## A propos 

Projet développé par **David Scanu**, étudiant en intelligence artificielle 🤖 à l'**École Microsoft IA par Simplon et ISEN**, 1ère promotion de Caen (2023-2024).

- [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davidscanu14/)
- [![image alt text](https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=dev.to&logoColor=white)](https://dev.to/davidscanu)
- [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://davidscanu.medium.com/)

### L’École IA Microsoft par Simplon et ISEN

L'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/) est une formation en **intelligence artificielle** offrant :

- une certification professionnelle reconnue par l'État (RNCP34757)
- une certification Agile
- deux certifications Microsoft Azure.

En 2018, Microsoft a créé cette école en partenariat avec Simplon, un réseau de fabriques numériques, pour offrir des opportunités d'emploi dans le domaine de l'IA. 
La formation comprend l'apprentissage des bases du développement, la maîtrise des données et la conception et le développement de modèles prédictifs de Machine Learning et de Deep Learning.

Cette formation s’effectue en deux temps: après avoir suivi une formation intensive de 7 mois, nous sommes entrés en contrat de professionnalisation de 14 mois en alternance au sein d’une entreprise locale.