import pandas as pd
import streamlit as st
import os

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.types import *
from sqlalchemy import text
from sqlalchemy import delete


# URL de la base de données, cachée dans un secret streamlit
DB_PSY_URI = st.secrets.DB_PSY_URI


# # 🔎 Inspect - Get Database Information
# inspector = inspect(engine)
# # Get tables information
# for table in inspector.get_table_names() :
#     print(table)


def insert_dataframe_to_table(df: pd.DataFrame, table_name:str, primary_key:str=None, if_exists='append'):
    """
    Sauvegarde un dataFrame dans un table de la base de données.

    Args:
        - df : Un DataFrame Pandas.
        - table_name : Le nom de la table ou sauvegarder les données.
        - primary_key : Colonne du DataFrame qui sera la clé primaire de la table.
        - if_exists : Comment se comporter si la table existe déjà. Par défaut, 'append' : insérer de nouvelles valeurs dans la table existante.
    """

    engine = create_engine(DB_PSY_URI)

    data_type = {
        'int64' : db.Integer(),
        'float64' : db.Float(),
        'object' : db.String(255),
        'datetime64[ns]' : db.DateTime(),
        'datetime64[ns, Europe/Paris]' : db.DateTime(),
        'datetime64[us]' : db.DateTime(),
        'datetime64[us, Europe/Paris]' : db.DateTime(),
        'bool' : db.Boolean(),
        'category' : db.String()
    }
    columns = df.columns
    df_dtypes = {column:data_type[str(df[column].dtype)] for column in columns}

    try:
        with engine.connect() as conn:
            df.to_sql(table_name, engine, if_exists=if_exists, index=False, dtype=df_dtypes)

            # Vérifie que la clé primaire n'existe pas déjà
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table = metadata.tables['app_img_original']

            if primary_key and len(inspect(table).primary_key.columns.values()) == 0 :
                query = f"""ALTER TABLE {table_name} ADD PRIMARY KEY ({primary_key});"""
                result = conn.execute(text(query))
                conn.commit()
            print(f"""Données ajoutées avec succès à la table '{table_name}'.""")
    except Exception as e:
        raise Exception(f"Unexpected error : {e}") from e


def from_table_to_dataframe(table_name, parse_dates=None):
    """
    Charge les données d'une table dans un DataFrame.

    Args : 
        - table_name : Nom de la table.
        - parse_dates : Noms de colonnes contenant des dates.

    Retourne :
        - un DataFrame
    """

    engine = create_engine(DB_PSY_URI)

    try :
        with engine.connect() as conn:
            df = pd.read_sql_table(table_name, conn, parse_dates=parse_dates)
            return df
    except Exception as e:
        raise Exception(f"Unexpected error: {e}") from e





def sql_query_to_dataframe(query: str):
    """
    Requete SQL Brute avec SQLAlchemy. 

    Args :
        - query : Requete SQL brute.
    """
    engine = create_engine(DB_PSY_URI)
    sql_query = text(query)
    with engine.connect() as conn, conn.begin():  
        df = pd.read_sql_query(sql_query, conn)
        return df


def if_table_exists(table_name):
    engine = create_engine(DB_PSY_URI)
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        return True
    else:
        return False    


def drop_table(table_name):
    """
    Effacer une table. 

    Args : 
        - table_name : Nom de la table.
    """
    engine = create_engine(DB_PSY_URI)
    if inspect(engine).has_table(table_name):
        try :
            metadata = MetaData()
            metadata.reflect(bind=engine)  
            table = metadata.tables[table_name]
            table.drop(engine)
            inspector = inspect(engine)
            if not table_name in inspector.get_table_names():
                st.success(f"Table {table_name} supprimée avec succès !")
                print(f"Table {table_name} supprimée avec succès !")
                print()

        except Exception as e:
            raise Exception(f"Unexpected error: {e}") from e
    else :
        print(f"La table '{table_name}' que vous supprimer n'existe pas.")


def erase_table(table_name):
    """
    Effacer toutes les lignes d'une table. 

    Args : 
        - table_name : Nom de la table.
    """
    engine = create_engine(DB_PSY_URI)
    if inspect(engine).has_table(table_name):
        try :
            metadata = MetaData()
            metadata.reflect(bind=engine)  
            table = metadata.tables[table_name]
            # table.drop(engine)
            delete_stmt = delete(table)
            with engine.connect() as conn:
                result = conn.execute(delete_stmt)
                conn.commit()
                print(f"{result.rowcount} lignes effacées de la table {table_name}.")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}") from e
    else :
        print(f"La table '{table_name}' dont vous souhaitez effacer les lignes n'existe pas.")