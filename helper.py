from ultralytics import YOLO
import time
import streamlit as st
import cv2
from pytube import YouTube
import os
import uuid
import datetime
import pytz
import pandas as pd


import settings
import database

def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model

def detection_job(res, uploaded_image, model, model_path, model_type, confidence):

    with st.status("Sauvegarde de la détection...", expanded=True) as status:

        # Table "app_users"
        fake_user_dict = {
            "user_id" : "davidscanu14@gmail.com",
            "user_pw" : "fake_pw",
            "user_name" : "David Scanu",
            "user_role" : "admin"
        }

        # Effectuer la prédiction
        # res = model.predict(uploaded_image, conf=confidence)

        # Tracer les résultats
        # img_plotted = res[0].plot()[:, :, ::-1]
        # Afficher l'image avec les boîtes de détection
        # st.image(img_plotted, caption='Image détectée', use_column_width=True)

        # Création des dossiers pour sauvegarder les images et les labels
        if not os.path.exists('detections/imgs-original'):
            os.makedirs(os.path.join("detections", "imgs-original"))
        if not os.path.exists('detections/imgs-detected'):
            os.makedirs(os.path.join("detections", "imgs-detected"))
        if not os.path.exists('detections/labels'):
            os.makedirs(os.path.join("detections", "labels"))

        # Identifiant unique
        detection_timezone = pytz.timezone('Europe/Paris')
        detection_datetime = datetime.datetime.now(detection_timezone) 
        UID = detection_datetime.strftime("%Y-%m-%d-%H%M%S")

        # IDs
        job_id = uuid.uuid4()
        og_id = uuid.uuid4()
        dt_id = uuid.uuid4()
        label_id = uuid.uuid4()

        # Table "app_detection_jobs"
        st.write("Sauvegarde de la tâche de détection.")
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
        st.write("Sauvegarde de l'image originale.")
        og_img_dict = {}
        og_img_dict['og_id'] = og_id
        og_img_dict['og_filename'] = f"{UID}-original.jpg"
        og_img_dict['og_filepath'] = f"detections/imgs-original/{og_img_dict['og_filename']}"
        og_img_dict['og_height'] = res[0].orig_shape[0]
        og_img_dict['og_width'] = res[0].orig_shape[1]
        # Sauvegarde dans la table
        og_img_df = pd.DataFrame(og_img_dict, index=[0])
        database.insert_dataframe_to_table(og_img_df, "app_imgs_original", "og_id", if_exists = 'append')
        # Sauvegarder le fichier image
        uploaded_image.save(og_img_dict['og_filepath'])

        # Table "app_imgs_detected"
        st.write("Sauvegarde de l'image des détections.")
        detected_img_dict = {}
        detected_img_dict['dt_id'] = dt_id
        detected_img_dict['dt_filename'] = f"{UID}-detected.jpg"
        detected_img_dict['dt_filepath'] = f"detections/imgs-detected/{detected_img_dict['dt_filename']}"
        # Sauvegarde dans la table
        detected_img_df = pd.DataFrame(detected_img_dict, index=[0])
        database.insert_dataframe_to_table(detected_img_df, "app_imgs_detected", "dt_id", if_exists = 'append')
        # Sauvegarder le fichier de l'image détectée
        res[0].save(filename=detected_img_dict['dt_filepath'])

        # Table "app_detection_labels"
        st.write("Sauvegarde des lables au format '.txt'.")
        label_dict = {}
        label_dict['label_id'] = label_id
        label_dict['label_filename'] = f"{UID}.txt"
        label_dict['label_filepath'] = f"detections/labels/{label_dict['label_filename']}"
        # Sauvegarde dans la table
        label_df = pd.DataFrame(label_dict, index=[0])
        database.insert_dataframe_to_table(label_df, "app_detection_labels", "label_id", if_exists = 'append')
        # Enregistre les prédictions dans un fichier txt.
        res[0].save_txt(label_dict['label_filepath'])

        # Table "app_detection_boxes"
        st.write("Sauvegarde des boîtes de détection.")
        # Nom des classes détectées par le modèle
        classes_dict = res[0].names
        # Boîtes de détection
        boxes = res[0].boxes
        boxes_dict_list = []
        for box in boxes:
            box_cpu = box.cpu()
            box_numpy = box_cpu.numpy()
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
            boxes_dict_list.append(box_dict)
        # Sauvegarder les boîtes de détection
        boxes_df = pd.DataFrame(boxes_dict_list)
        database.insert_dataframe_to_table(boxes_df, "app_detection_boxes", "box_id", if_exists = 'append')

        status.update(label="Tâche de détection terminée !", state="complete", expanded=False)
        print(f"Tâche de détection terminé ! Job ID : '{job_id}'.")
        return job_id

def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None

def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)

    # # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Vidéo détectée',
                   channels="BGR",
                   use_column_width=True
                   )

def play_youtube_video(conf, model):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_youtube = st.sidebar.text_input("URL de la vidéo YouTube")

    is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button('Lancer la détection', use_container_width=True):
        try:
            yt = YouTube(source_youtube)
            stream = yt.streams.filter(file_extension="mp4", res=720).first()
            vid_cap = cv2.VideoCapture(stream.url)

            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker,
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Erreur de chargement de la vidéo : " + str(e))

def play_rtsp_stream(conf, model):
    """
    Plays an rtsp stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_rtsp = st.sidebar.text_input("URL du flux RTSP :")
    st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Lancer la détection', use_container_width=True):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    # vid_cap = cv2.VideoCapture(source_rtsp)
                    # time.sleep(0.1)
                    # continue
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Erreur lors du chargement du flux RTSP : " + str(e))

def play_webcam(conf, model):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Lancer la détection', use_container_width=True):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker,
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Erreur de chargement de la vidéo : " + str(e))

def play_stored_video(conf, model):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_vid = st.sidebar.selectbox(
        "Choisissez une vidéo...", settings.VIDEOS_DICT.keys())

    is_display_tracker, tracker = display_tracker_options()

    with open(settings.VIDEOS_DICT.get(source_vid), 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.sidebar.button('Lancer la détection', use_container_width=True):
        try:
            vid_cap = cv2.VideoCapture(
                str(settings.VIDEOS_DICT.get(source_vid)))
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Erreur de chargement de la vidéo : " + str(e))


# DELETE
            
def delete_dir_files(directory_path):
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            os.remove(os.path.join(directory_path, filename))
    print(f"Suppression de tous les fichiers de '{directory_path}'.")

def clear_past_detections_files(dir_path):
    for root, sub_dir_names, files in os.walk(dir_path):
        for sub_dir_name in sub_dir_names:
            sub_dir_path = os.path.join(root, sub_dir_name)
            if os.path.isdir(sub_dir_path):
                for filename in os.listdir(sub_dir_path):
                    filename_path = os.path.join(sub_dir_path, filename)
                    if os.path.isfile(filename_path):
                        os.remove(filename_path)
                print(f"Suppression de tous les fichiers de '{sub_dir_path}'.")


# DISPLAY
                
def display_detection_imgs(job_id):

    # Requete jointe pour afficher les détections passées
    job_query = f"""
        SELECT * FROM app_detection_jobs
        JOIN app_imgs_original
        ON job_og_id = og_id
        JOIN app_imgs_detected
        ON job_dt_id = dt_id
        WHERE job_id = '{job_id}';
        """
    job_df = database.sql_query_to_dataframe(job_query)
    
    if not job_df.empty :
        job_dict = job_df.to_dict('records')[0]

        col1, col2 = st.columns(2)
        with col1 : 
            if os.path.isfile(job_dict['og_filepath']):
                # st.subheader(job_dict['og_filename'])
                st.image(job_dict['og_filepath'])
        with col2 :
            if os.path.isfile(job_dict['dt_filepath']):
                # st.subheader(job_dict['dt_filename'])
                st.image(job_dict['dt_filepath'])

def display_detection_details(job_id):

    # Job de détection
    job_query = f"""
        SELECT *
        FROM app_detection_jobs
        JOIN app_imgs_original
        ON job_og_id = og_id
        JOIN app_imgs_detected
        ON job_dt_id = dt_id
        WHERE job_id = '{job_id}';
        """
    job_df = database.sql_query_to_dataframe(job_query)
    if not job_df.empty:
        job_dict = job_df.to_dict('records')[0]
        # Detection Boxes
        boxes_query = f"""
            SELECT * FROM app_detection_boxes
            WHERE box_job_id = '{job_id}';
            """
        boxes_df = database.sql_query_to_dataframe(boxes_query)
        if not boxes_df.empty :
            st.markdown(f"""
                - **Modèle** : {job_dict['job_model_filename']}
                - **Tâche** : {job_dict['job_task']}
                - **Seuil de confiance** : {job_dict['job_confidence']}
                - **Vitesse de détection** : {round(job_dict['job_speed'], 2)} ms
                - **Nombre de boîtes de détection** : {len(boxes_df)}
                - **Nombre de classes différentes** : {boxes_df['box_class_id'].nunique()}
                - **Liste des classes détectées** : {boxes_df['box_class_name'].unique().tolist()}
                - **Nom de l'image originale** : {job_dict['og_filename']}
                - **Nom de l'image détectée** : {job_dict['dt_filename']}
                - **Date de détection** : {job_dict['job_created_at'].strftime('%Y-%m-%d %X')}   
            """)

def display_detection_boxes(job_id):
    # Detection Boxes
    boxes_sql_query = f"""
        SELECT * FROM app_detection_boxes
        WHERE box_job_id = '{job_id}'
        """
    detections_boxes_df = database.sql_query_to_dataframe(boxes_sql_query)
    if not detections_boxes_df.empty:
        st.markdown("""##### 📦 Boîtes de détection""")
        st.dataframe(detections_boxes_df[['box_class_name', 'box_class_id', 'box_conf', 'box_x_center', 'box_y_center', 'box_width', 'box_height']])