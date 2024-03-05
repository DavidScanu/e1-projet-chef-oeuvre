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
    past_detections_df.sort_values(by='pred_created_at', ascending=False, inplace=True, ignore_index=True)
    # Conversion de la date au bon Timezone
    past_detections_df['pred_created_at'] = past_detections_df['pred_created_at'].dt.tz_convert(tz='Europe/Paris')

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
                with open(past_detections_df.loc[i, 'pred_filepath']) as f:
                    # lecture des lignes dans le fichier texte
                    lines = f.readlines()
                    detections_list = []
                    for line in lines:
                        # print("Line{}: {}".format(count, line.strip()))
                        line_splitted = line.strip().split(" ")
                        detections_list.append(line_splitted)

                    # class x_center y_center width height
                    detections_df = pd.DataFrame(detections_list, columns=['class', 'x_center', 'y_center', 'width', 'height'])

                st.markdown(f"""
                    - **Date de détection** : {past_detections_df.loc[i, 'pred_created_at'].strftime('%Y-%m-%d %X')}
                    - **Vitesse de détection** : {round(past_detections_df.loc[i, 'pred_speed'], 2)} ms
                    - **Nombre de classes d'objets différentes** : {detections_df['class'].nunique()}
                    - **Nombre de boîtes de détection** : {len(detections_df)}
                """)
                st.markdown("""##### 📦 Boîtes de détection""")
                st.dataframe(detections_df)
        

if st.button('🗑️ Effacer les détections passées', type="primary", on_click=click_erase_button): 
    with st.spinner('Tâche en cours...'):
        database.erase_table("app_img_original")
        delete_all_files("detections/imgs-original")
        database.erase_table("app_img_detected")
        delete_all_files("detections/imgs-detected")
        database.erase_table("app_pred_boxes")
        delete_all_files("detections/pred")


# if st.button('⚠️ Supprimer toutes les tables', type="primary", on_click=click_erase_button): 
#     with st.spinner('Tâche en cours...'):
#         database.drop_table("app_img_original")
#         delete_all_files("detections/imgs-original")
#         database.drop_table("app_img_detected")
#         delete_all_files("detections/imgs-detected")
#         database.drop_table("app_pred_boxes")
#         delete_all_files("detections/pred")