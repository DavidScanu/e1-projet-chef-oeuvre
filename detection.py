# Python In-built packages
import datetime
import pytz
from pathlib import Path
import PIL
import os
import uuid

# External packages
import streamlit as st
import pandas as pd

# Local Modules
import settings
import helper
import database

# Variables

# Table "app_users"
fake_user_dict = {
    "user_id" : "davidscanu14@gmail.com",
    "user_pw" : "fake_pw",
    "user_name" : "David Scanu",
    "user_role" : "admin"
}


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

def click_detect_button():
    st.session_state.data_erased = False
    
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


    with st.container(border=True):
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
                if st.sidebar.button('Lancer la détection', on_click=click_detect_button):

                    # Effectuer la prédiction
                    res = model.predict(uploaded_image, conf=confidence)

                    # Identifiant unique
                    detection_timezone = pytz.timezone('Europe/Paris')
                    detection_datetime = datetime.datetime.now(detection_timezone) 
                    UID = detection_datetime.strftime("%Y-%m-%d-%H%M%S")

                    job_id = uuid.uuid4()
                    og_id = uuid.uuid4()
                    dt_id = uuid.uuid4()
                    label_id = uuid.uuid4()


                    # Table "app_detection_jobs"
                    job_dict = {}
                    job_dict['job_id'] = job_id
                    job_dict['job_speed'] = float(sum(res[0].speed.values())) # vitesse de détection en ms
                    job_dict['job_confidence'] = confidence
                    job_dict['job_task'] = model_type
                    job_dict['job_count'] = len(res[0].boxes)
                    job_dict['job_model_filename'] = os.path.basename(str(model_path))
                    job_dict['job_model_weights_path'] = str(model_path)
                    # clés étrangères
                    job_dict['job_og_id'] = og_id
                    job_dict['job_dt_id'] = dt_id
                    job_dict['job_label_id'] = label_id
                    job_dict['job_user_id'] = fake_user_dict['user_id']
                    # Sauvegarde dans la table
                    job_df = pd.DataFrame(job_dict, index=[0])
                    job_df['job_created_at'] = pd.Timestamp.now(tz="Europe/Paris")
                    database.insert_dataframe_to_table(job_df, "app_detection_jobs", "job_id", if_exists = 'append')

                    # Table "app_imgs_original"
                    og_img_dict = {}
                    og_img_dict['og_id'] = og_id
                    og_img_dict['og_filename'] = f"{og_img_dict['og_id']}-original.jpg"
                    og_img_dict['og_filepath'] = f"detections/imgs-original/{og_img_dict['og_filename']}"
                    og_img_dict['og_height'] = res[0].orig_shape[0]
                    og_img_dict['og_width'] = res[0].orig_shape[1]
                    # Sauvegarde dans la table
                    og_img_df = pd.DataFrame(og_img_dict, index=[0])
                    database.insert_dataframe_to_table(og_img_df, "app_imgs_original", "og_id", if_exists = 'append')
                    # Sauvegarder le fichier image
                    uploaded_image.save(og_img_dict['og_filepath'])

                    # Table "app_imgs_detected"
                    detected_img_dict = {}
                    detected_img_dict['dt_id'] = dt_id
                    detected_img_dict['dt_filename'] = f"{detected_img_dict['dt_id']}-detected.jpg"
                    detected_img_dict['dt_filepath'] = f"detections/imgs-detected/{detected_img_dict['dt_filename']}"
                    # Sauvegarde dans la table
                    detected_img_df = pd.DataFrame(detected_img_dict, index=[0])
                    database.insert_dataframe_to_table(detected_img_df, "app_imgs_detected", "dt_id", if_exists = 'append')
                    # Tracer les résultats et sauvegarder le fichier de l'image détectée
                    img_plotted = res[0].plot(save=True, filename=detected_img_dict['dt_filepath'])[:, :, ::-1]

                    # Table "app_detection_labels"
                    label_dict = {}
                    label_dict['label_id'] = label_id
                    label_dict['label_filename'] = f"{label_dict['label_id']}.txt"
                    label_dict['label_filepath'] = f"detections/labels/{label_dict['label_filename']}"
                    # Sauvegarde dans la table
                    label_df = pd.DataFrame(label_dict, index=[0])
                    database.insert_dataframe_to_table(label_df, "app_detection_labels", "label_id", if_exists = 'append')
                    # Enregistre les prédictions dans un fichier txt.
                    res[0].save_txt(label_dict['label_filepath'])

                    # Afficher l'image avec les boîtes de détection
                    st.image(img_plotted, caption='Image détectée', use_column_width=True)
        
                    # Nom des classes détectées par le modèle
                    classes_dict = res[0].names

                    # Boîtes de détection
                    boxes = res[0].boxes
                    boxes_list = []

                    # Table "app_detection_boxes"
                    for box in boxes:
                        box_numpy = box.numpy()
                        box_xywhn = box_numpy.xywhn.tolist()

                        box_dict = {}
                        box_dict['box_id'] = uuid.uuid4()
                        box_dict['box_class_id'] = int(box_numpy.cls.tolist()[0])
                        box_dict['box_class_name'] =  classes_dict[int(box_numpy.cls.tolist()[0])]
                        box_dict['box_x_center'] = box_xywhn[0][0]
                        box_dict['box_y_center'] = box_xywhn[0][1]
                        box_dict['box_width'] = box_xywhn[0][2]
                        box_dict['box_height'] = box_xywhn[0][3]
                        box_dict['box_conf'] = round(box_numpy.conf.tolist()[0], 4)
                        box_dict['box_label_id'] = label_id
                        box_dict['box_job_id'] = job_id

                        boxes_list.append(box_dict)

                        # for k, v in box_dict.items():
                        #     print(f"{k} : {v}")

                        box_df = pd.DataFrame(box_dict, index=[0])
                        database.insert_dataframe_to_table(box_df, "app_detection_boxes", "box_id", if_exists = 'append')

                    # Afficher les boxes sur la page "Détection"
                    boxes_df = pd.DataFrame(boxes_list)
                    try:
                        with st.expander("Résultats de détection"):
                            st.dataframe(boxes_df[['box_class_id', 'box_class_name', 'box_conf', 'box_x_center', 'box_y_center', 'box_width', 'box_height']])
                            # for box in boxes:
                            #     st.write(box.data)
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
    st.error("Veuillez sélectionner un type de source valide !")
