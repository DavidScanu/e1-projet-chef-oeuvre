# External packages
import streamlit as st

# Setting page layout
st.set_page_config(
    page_title="About",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Main page heading
st.title("👋 A propos")

# Sidebar
st.sidebar.header("🛠️ Outils")

st.sidebar.markdown(
    """
    Ce projet utilise les outils innovants suivants :
    - 💻 [Codespaces](https://github.com/features/codespaces)
    - 🕶️ [Streamlit](https://streamlit.io/)
    - ⚡ [Yolov8](https://docs.ultralytics.com/fr) ([Ultralytics](https://www.ultralytics.com/fr))
    - 🧪 [Autodistill](https://docs.autodistill.com/) ([Roboflow](https://roboflow.com/))
    """
)



"""
Ce projet chef-d'œuvre (réf. E1) témoigne de la maîtrise des compétences visées pour l'obtention du titre professionnel : [Développeur en intelligence artificielle (RNCP 34757)](https://www.francecompetences.fr/recherche/rncp/34757/), délivré par [Simplon](https://simplon.co/), dans le cadre de l'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/). Ce projet chef-d'œuvre implique la création d'un programme d'intelligence artificielle complet, ainsi que le développement d'une application web qui le déploie.

> 🎓 Projet développé par [David Scanu](https://www.linkedin.com/in/davidscanu14/), étudiant en intelligence artificielle 🤖 à l'[École Microsoft IA Caen par Simplon et ISEN](https://isen-caen.fr/ecole-ia-microsoft-by-simplon-et-isen-ouest/), 1ère promotion de Caen (2023-2024).

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

### GitHub

Le code pour ce projet est disponible dans [ce dépôt GitHub](https://github.com/DavidScanu/e1-projet-chef-oeuvre). 

"""