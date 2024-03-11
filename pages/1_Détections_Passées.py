# Python In-built packages
import os

# External packages
import streamlit as st
import pandas as pd

# Local Modules
import database
from helper import delete_dir_files, clear_past_detections_files, display_detection_imgs, display_detection_details, display_detection_boxes

# Setting page layout
st.set_page_config(
    page_title="Détections passées",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.header("🖼️ Détections passées", divider="rainbow")


# Si la table existe
if database.if_table_exists("app_detection_jobs"):
    # Requete jointe pour afficher les détections passées
    sql_query = """
        SELECT job_id, job_created_at
        FROM app_detection_jobs
        """
    past_detections_df = database.sql_query_to_dataframe(sql_query)
else: 
    past_detections_df = pd.DataFrame() # DataFrame vide, évite l'erreur avec 'None'


# Session state
if 'data_erased' not in st.session_state:
    st.session_state.data_erased = False

def click_erase_button():
    st.session_state.data_erased = True

if st.session_state.data_erased:
    past_detections_df = pd.DataFrame()
    st.error('Toutes les détections passées sont effacées !', icon="👏")


# Si le DataFrame des détections passées est vide
if past_detections_df.empty:
    st.warning("Aucunes détections sauvegardées. Veuillez réaliser votre première détection sur la page **Détection**.")
else:

    # Conversion de la date au bon Timezone
    past_detections_df['job_created_at'] = past_detections_df['job_created_at'].dt.tz_convert(tz='Europe/Paris')
    # Trier par dates, les plus récents en premier
    past_detections_df.sort_values(by='job_created_at', ascending=False, inplace=True, ignore_index=True)

    for i in range(len(past_detections_df)):
        with st.container(border=True):

            display_detection_imgs(job_id=past_detections_df.loc[i, 'job_id'])

            with st.expander("📝 Détails de la détection"):
                # Détails de la détection
                display_detection_details(job_id=past_detections_df.loc[i, 'job_id'])
                # Boîtes de détection
                display_detection_boxes(job_id=past_detections_df.loc[i, 'job_id'])

            # Ajouter "Ratings" ici 
            # Si le vote n'existe pas pour ce 'job_id' alors proposer le widget de vote
            # Sinon afficher la note donnée



# Effacer ou supprimer les détections passées
tables_list = [
    "app_detection_jobs",
    "app_imgs_original",
    "app_imgs_detected",
    "app_detection_labels",
    "app_detection_boxes"
]

for table in tables_list:
    database.drop_table(table)
clear_past_detections_files("detections")

if st.button('🗑️ Effacer les détections passées', type="primary", on_click=click_erase_button): 
    with st.spinner('Tâche en cours...'):
        for table in tables_list:
            database.erase_table(table)
        clear_past_detections_files("./detections")

if st.button('⚠️ Supprimer toutes les tables', type="primary", on_click=click_erase_button): 
    with st.spinner('Tâche en cours...'):
        for table in tables_list:
            database.drop_table(table)
        clear_past_detections_files("detections")
