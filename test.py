from unittest import TestCase, main 
import streamlit as st 
from ultralytics import YOLO

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

import database 
import os

import settings
from pathlib import Path

class TestDev(TestCase):
    # Vérifie si ces fichiers sont dans le dossier racine
    def test_root_files(self):
        root_dir_files = os.listdir()
        self.assertIn("detection.py", root_dir_files)
        self.assertIn("helper.py", root_dir_files)
        self.assertIn("settings.py", root_dir_files)
        self.assertIn("database.py", root_dir_files)
        self.assertIn(".gitignore", root_dir_files)
        self.assertIn("requirements.txt", root_dir_files)

    # Vérifie 
    def test_weights_files(self):
        weights_dir_files = os.listdir("./weights")
        self.assertIn("yolov8n.pt", weights_dir_files)
        self.assertIn("yolov8n-seg.pt", weights_dir_files)

class TestDatabase(TestCase):

    # Vérifier connection à la base de données
    def test_connection(self):

        DB_PSY_URI = st.secrets.DB_PSY_URI
        self.assertIsNotNone(DB_PSY_URI)

        engine = create_engine(DB_PSY_URI)
        self.assertIsInstance(engine, Engine)

class TestLoadModel(TestCase):
    # Vérifier le chargement des poids dans le modèle Yolo
    def test_load_detection_model(self):
        model_path = Path(settings.DETECTION_MODEL)
        model = YOLO(model_path)
        self.assertIsInstance(model, YOLO)

    def test_load_segmentation_model(self):
        model_path = Path(settings.SEGMENTATION_MODEL)
        model = YOLO(model_path)
        self.assertIsInstance(model, YOLO)


if __name__  == '__main__':
    main(verbosity=2)