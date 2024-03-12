# Python In-built packages
import datetime
import pytz
from pathlib import Path
import PIL
import os
import uuid
import time 

# External packages
import streamlit as st
from streamlit_star_rating import st_star_rating
import pandas as pd

# Local Modules
import settings
import helper
import database

# Setting page layout
st.set_page_config(
    page_title="Détection d'objets avec YOLOv8",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Session state
if 'data_erased' not in st.session_state:
    st.session_state.data_erased = False

def on_click_detect_button():
    st.session_state.data_erased = False

if 'job_id' not in st.session_state:
    st.session_state['job_id'] = None

def on_change_source_img():
    st.session_state['job_id'] = None


# def on_click_rating(value, **on_click_kwargs_dict):
#     st.session_state['rating'] = value
#     st.session_state['dr_job_id'] = on_click_kwargs_dict['dr_job_id']


# if 'run' not in st.session_state:
#     st.session_state['run'] = 0

# print("-------")
# print(f"This is a run : {st.session_state['run']}")
# print("-------")

# st.session_state['run'] = st.session_state['run'] + 1


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
        "Choisissez une image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'), on_change=on_change_source_img)

    if source_img is None:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:
                try:
                    default_image_path = str(settings.DEFAULT_IMAGE)
                    default_image = PIL.Image.open(default_image_path)
                    st.image(default_image_path, caption="Image par défaut",
                            use_column_width=True)
                except Exception as ex:
                    st.error("Une erreur s'est produite lors de l'ouverture de l'image.")
                    st.error(ex)
            with col2:
                default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(
                    default_detected_image_path)
                st.image(default_detected_image_path, caption='Exemple de détection',
                        use_column_width=True)

    else :

        with st.container(border=True):

            col1, col2 = st.columns(2)

            uploaded_image = PIL.Image.open(source_img)
            # Montrer l'image
            col1.image(source_img, caption="Image originale",
                    use_column_width=True) 

            if st.sidebar.button('Lancer la détection', on_click=on_click_detect_button, use_container_width=True):

                # # Effectuer la prédiction
                res = model.predict(uploaded_image, conf=confidence)
                # # Tracer les résultats
                img_plotted = res[0].plot()[:, :, ::-1]
                # # Afficher l'image avec les boîtes de détection
                col2.image(img_plotted, caption='Image détectée', use_column_width=True)

                # with st.spinner('Sauvegarde des informations de détection...'):

                job_id = helper.detection_job(res, uploaded_image, model, model_path, model_type, confidence)
                # Actualisation de l'état de la session (Session State)
                st.session_state['job_id'] = job_id

                with st.expander("📝 Résultats de détection"):
                    # Détails de la détection
                    helper.display_detection_details(job_id)
                    # Boîtes de détection
                    helper.display_detection_boxes(job_id)
            
            if st.session_state['job_id']:
                placeholder = st.empty()

                with placeholder.container():

                    stars = st_star_rating("Notez cette détection !", 5, 3, 20, key="rating_widget")

                    if st.button('Submit'):
                        with placeholder.container():
                            rating_dict = {}
                            rating_dict['dr_id'] = uuid.uuid4()
                            rating_dict['dr_rating'] = stars
                            rating_dict['dr_job_id'] = st.session_state['job_id']
                            # st.json(rating_dict)
                            print(rating_dict)

                            # Sauvegarde
                            feedback_df = pd.DataFrame(rating_dict, index=[0])
                            database.insert_dataframe_to_table(feedback_df, "app_detection_ratings", "dr_id", if_exists = 'append')
                            st.success(f"Merci d'avoir voté {stars} étoiles pour cette détection !")
                            # st.write(f"job_id is : {rating_dict['dr_job_id']}")


elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Veuillez sélectionner un type de source valide !")



st.write(st.session_state)
