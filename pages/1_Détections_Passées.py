# Python In-built packages
import os

# External packages
import streamlit as st
import pandas as pd

# Local Modules
import database

# Utilities
def delete_all_files(directory_path):
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            os.remove(os.path.join(directory_path, filename))
    print(f"Tous les fichiers effacés de '{directory_path}'.")


# Setting page layout
st.set_page_config(
    page_title="Détections passées",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("🖼️ Détections passées")



# Si la table existe
if database.if_table_exists("app_img_original"):
    # Requete jointe pour afficher les détections passées
    sql_query = """
        SELECT * FROM app_img_original
        JOIN app_img_detected
        ON app_img_original.og_id = app_img_detected.dt_og_img_id
        JOIN app_pred_boxes
        ON app_img_original.og_id = app_pred_boxes.pred_og_img_id
        """

    past_detections_df = database.sql_query_to_dataframe(sql_query)
else: 
    past_detections_df = pd.DataFrame()



if past_detections_df.empty:
    st.warning("⚠️ Aucunes détections pour l'instant. Veuillez réaliser votre première dtection sur la page **Détection**.")
else:

    st.write(past_detections_df)

    past_detections_dict = past_detections_df.to_dict('records')
    for detection in past_detections_dict : 


        print("Detection : ", detection)
        st.subheader(f"Hello")
        col1, col2 = st.columns(2)
        with col1 : 
            st.image(detection['og_filepath'])
        with col2 :
            st.image(detection['dt_filepath'])


    if st.button('🗑️ Effacer les détections passées', type="primary"): 

        with st.spinner('Tâche en cours...'):

            database.erase_table("app_img_original")
            delete_all_files("detections/imgs-original")

            database.erase_table("app_img_detected")
            delete_all_files("detections/imgs-detected")

            database.erase_table("app_pred_boxes")
            delete_all_files("detections/pred")

        st.success('Toutes les détections passées sont effacées !', icon="👏")