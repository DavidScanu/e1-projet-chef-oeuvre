import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.types import *
from sqlalchemy import text
from sqlalchemy import delete

# print(db.__version__)

# URL de la base de données, cachée dans un secret streamlit
# https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
DB_PSY_URI = "postgresql+psycopg://fapqxaxqwmkixa:62785e5a8838c3dd8f9abb0a4fc7aaabc2854335b248206377d2dea49d73d2e4@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/d7dqlblubkaglv"


# for table in inspector.get_table_names() :
#     print(table)

# Get column information
# for column in inspector.get_columns('app_img_original') :
#     print(column)

engine = create_engine(DB_PSY_URI)

# Create a MetaData instance
metadata = MetaData()
# reflect db schema to MetaData
metadata.reflect(bind=engine)

# with engine.connect() as con:

#     stmt = text("""
#         SELECT * FROM app_img_original
#         JOIN app_img_detected
#         ON app_img_original.id = app_img_detected.og_img_id
#         JOIN app_pred_boxes
#         ON app_img_original.id = app_pred_boxes.og_img_id
#         """)
#     res = con.execute(stmt)
#     for _row in res:
#         print(_row)



