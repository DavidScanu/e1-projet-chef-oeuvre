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
    print(f"Suppression de tous les fichiers de '{directory_path}'.")


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

    # Trier par dates, du plus récent
    past_detections_df.sort_values(by='job_created_at', ascending=False, inplace=True, ignore_index=True)
    # Conversion de la date au bon Timezone
    past_detections_df['job_created_at'] = past_detections_df['job_created_at'].dt.tz_convert(tz='Europe/Paris')

    for i in range(len(past_detections_df)):
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1 : 
                # st.subheader(past_detections_df.loc[i, 'og_filename'])
                st.image(past_detections_df.loc[i, 'og_filepath'])
            with col2 :
                # st.subheader(past_detections_df.loc[i, 'dt_filename'])
                st.image(past_detections_df.loc[i, 'dt_filepath'])

            with st.expander("📝 Détails de la détection"):

                # Detection Boxes
                boxes_sql_query = f"""
                    SELECT * FROM app_detection_boxes
                    WHERE box_job_id = '{past_detections_df.loc[i, 'job_id']}'
                    """
                detections_boxes_df = database.sql_query_to_dataframe(boxes_sql_query)

                # detection_misc_info_dict = {
                #     "Nom de l'image originale" : past_detections_df.loc[i, 'og_filename'],
                #     "Nom de l'image détectée" : past_detections_df.loc[i, 'dt_filename'],
                #     "Date de détection" : past_detections_df.loc[i, 'job_created_at'],
                #     "Vitesse de détection" : round(past_detections_df.loc[i, 'job_speed'], 2),
                #     "Nombre de classes d'objets différentes" : detections_boxes_df['box_class_id'].nunique(),
                #     "Nombre de boîtes de détection" : len(detections_boxes_df)
                # }
                # detection_misc_info_dict_converted = {
                #     'Description' : [k for k in detection_misc_info_dict.keys()],
                #     'Valeur' : [v for v in detection_misc_info_dict.values()]
                # }
                # detection_misc_info_df = pd.DataFrame(detection_misc_info_dict_converted)
                # st.dataframe(detection_misc_info_df)

                st.markdown(f"""
                    - **Date de détection** : {past_detections_df.loc[i, 'job_created_at'].strftime('%Y-%m-%d %X')}   
                    - **Nom de l'image originale** : {past_detections_df.loc[i, 'og_filename']}
                    - **Nom de l'image détectée** : {past_detections_df.loc[i, 'dt_filename']}
                    - **Vitesse de détection** : {round(past_detections_df.loc[i, 'job_speed'], 2)} ms
                    - **Nombre de classes d'objets différentes** : {detections_boxes_df['box_class_id'].nunique()}
                    - **Nombre de boîtes de détection** : {len(detections_boxes_df)}
                """)
                st.markdown("""##### 📦 Boîtes de détection""")
                st.dataframe(detections_boxes_df[['box_class_name', 'box_class_id', 'box_conf', 'box_x_center', 'box_y_center', 'box_width', 'box_height']])


            # Ajouter "Ratings" ici 
            # Si le vote n'existe pas pour ce 'job_id' alors proposer le widget de vote
            # Sinon afficher la note donnée
            st.write(past_detections_df.loc[i, 'job_id'])

if st.button('🗑️ Effacer les détections passées', type="primary", on_click=click_erase_button): 
    with st.spinner('Tâche en cours...'):
        database.erase_table("app_detection_jobs")
        database.erase_table("app_imgs_original")
        delete_all_files("detections/imgs-original")
        database.erase_table("app_imgs_detected")
        delete_all_files("detections/imgs-detected")
        database.erase_table("app_detection_labels")
        delete_all_files("detections/labels")
        database.erase_table("app_detection_boxes")

if st.button('⚠️ Supprimer toutes les tables', type="primary", on_click=click_erase_button): 
    with st.spinner('Tâche en cours...'):
        database.drop_table("app_detection_jobs")
        database.drop_table("app_imgs_original")
        delete_all_files("detections/imgs-original")
        database.drop_table("app_imgs_detected")
        delete_all_files("detections/imgs-detected")
        database.drop_table("app_detection_labels")
        delete_all_files("detections/labels")
        database.drop_table("app_detection_boxes")