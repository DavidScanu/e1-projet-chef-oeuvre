import pandas as pd
import streamlit as st
import os

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Table

print(db.__version__)

# URL de la base de données, cachée dans un secret streamlit
# https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
DB_PSY_URI = st.secrets.DB_PSY_URI

engine = create_engine(DB_PSY_URI)

# 🔎 Inspect - Get Database Information
inspector = inspect(engine)
# Get tables information
for table in inspector.get_table_names() :
    print(table)



# Créer une page détections passées avec image, images détectée, boxes

# 1 image, plusieurs détections 
# Table "app_images"
# Table "app_images_detected"
# Table "app_detections"
    
# Save détection
    
# Load past détections
    





# table "Users"
# - login
# - mot de passe