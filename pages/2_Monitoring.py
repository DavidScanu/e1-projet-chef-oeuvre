import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import database


# Setting page layout
st.set_page_config(
    page_title="Monitoring",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.header("📊 Monitoring", divider="rainbow")

# --- Authentication ---
from helper import authentification_main
authentification_main()

# Si la table existe
if database.if_table_exists("app_detection_jobs"):
    # Requete jointe pour afficher les détections passées
    sql_query = """
        SELECT * FROM app_detection_jobs
        JOIN app_imgs_original
        ON job_og_id = og_id
        JOIN app_imgs_detected
        ON job_dt_id = dt_id
        JOIN app_detection_labels
        ON job_label_id = label_id
        """
    past_detections_df = database.sql_query_to_dataframe(sql_query)
else: 
    past_detections_df = pd.DataFrame() # DataFrame vide, évite l'erreur avec 'None'


# Detection Boxes
detections_boxes_df = database.from_table_to_dataframe('app_detection_boxes')


if past_detections_df.empty:
    st.warning("Aucunes détections sauvegardées. Veuillez réaliser votre première détection sur la page **Détection**.")
else:

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns(4)

        # Nombre de détections
        job_count = past_detections_df['job_id'].nunique()
        col1.metric('Nombre de tâches de détections', job_count)
        # Moyenne nombre de détection par image
        job_count_mean = round(past_detections_df['job_count'].mean(), 2)
        col2.metric('Nombre de détections par image', job_count_mean)
        # Vitesses moyenne de détection
        job_speed_mean = round(past_detections_df['job_speed'].mean(), 2)
        col3.metric('Vitesse moyenne de détection', f"{job_speed_mean} ms")
        # Score moyen des détections 
        box_conf_mean = round(detections_boxes_df['box_conf'].mean(), 4) * 100 
        col4.metric('Score de confiance moyen', f"{box_conf_mean} %")
        # Nombre de détections par jour

        # Votes / Ratings

    # - Histogramme nombre de détection chaque jour
    # - Histogramme moyenne de score des détections
    # - Histogramme détections par classes (ou camembert)


    # Définir des seuils d'alerte
    # Envoie automatisé




    # st.subheader('Détections')
    # st.dataframe(past_detections_df)
    
    # st.subheader('Boxes')
    # st.dataframe(detections_boxes_df)