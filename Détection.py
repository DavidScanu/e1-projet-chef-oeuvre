# Python In-built packages
import datetime
import pytz
from pathlib import Path
import PIL

# External packages
import streamlit as st

# # Local Modules
import settings
import helper



# Setting page layout
st.set_page_config(
    page_title="Détection d'objets avec YOLOv8",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.header("👁️ Détection d'objets avec YOLOv8", divider="rainbow")

# Sidebar
st.sidebar.header("⚗️ Configuration du modèle")

# Model Options
model_type = st.sidebar.radio(
    "Selectionnez une tâche", ['Détection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "Selection confiance du modèle", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Détection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Impossible de charger le modèle. Vérifiez le chemin : '{model_path}'")
    st.error(ex)

st.sidebar.header("🖼️📽️ Source")
source_radio = st.sidebar.radio(
    "Selectionnez une source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choisissez une image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Image par défaut",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                # Montrer l'image
                st.image(source_img, caption="Image originale",
                         use_column_width=True)
        except Exception as ex:
            st.error("Une erreur s'est produite lors de l'ouverture de l'image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Exemple de détection',
                     use_column_width=True)
        else:
            if st.sidebar.button('Lancer la détection'):
                # Effectuer la prédiction
                res = model.predict(uploaded_image, conf=confidence)
                # Identifiant unique
                UID = datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d-%H%M%S")
                original_img_filepath = f"images/uploaded/{UID}-original.jpg"
                detected_img_filepath = f"images/detected/{UID}-detected.jpg"
                # Sauvegarder l'image dans "images/uploaded"
                uploaded_image.save(original_img_filepath)
                # Boîtes de détection
                boxes = res[0].boxes
                # Tracer les résultats et sauvegarder l'image détectée dans "images/detected"
                res_plotted = res[0].plot(save=True, filename=detected_img_filepath)[:, :, ::-1]
                # Afficher l'image avec les boîtes de détection
                st.image(res_plotted, caption='Image détectée',
                         use_column_width=True)
                try:
                    with st.expander("Résultats de détection"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("Aucune image n'a encore été téléchargée !")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Veuillez sélectionner un type de source valide !")
