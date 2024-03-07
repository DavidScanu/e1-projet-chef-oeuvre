import streamlit as st
import pandas as pd

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



# Page : Reporting / monitoring

# - nombre total d'images détectées
# - combien de détections totales
# - moyenne nombre de détection par image
# - vitesses moyenne de détection
# - score moyen des détections 

# - nombre de détections par jour
# - histogramme nombre de détection chaque jour

# - nombre de détection par classe

# - Performances du modèles ??? 

# Définir des seuils d'alerte
# Envoie automatisé


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
    st.subheader('Détections')
    st.dataframe(past_detections_df)
    
    st.subheader('Boxes')

    st.dataframe(detections_boxes_df)

