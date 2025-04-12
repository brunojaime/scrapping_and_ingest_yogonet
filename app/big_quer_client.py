import os
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from dotenv import load_dotenv

load_dotenv() 

# Leer variables desde entorno (.env o Docker)
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Setear credenciales explícitamente
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def ensure_dataset(client: bigquery.Client):
    dataset_ref = client.dataset(DATASET_ID)

    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset '{DATASET_ID}' ya existe.")
    except NotFound:
        print(f"Dataset '{DATASET_ID}' no existe. Creando...")
        dataset = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
        client.create_dataset(dataset)
        print("Dataset creado correctamente.")

def ensure_table(client: bigquery.Client):
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

    try:
        client.get_table(table_ref)
        print(f"Tabla '{TABLE_ID}' ya existe.")
    except NotFound:
        print(f"Tabla '{TABLE_ID}' no existe. Creando...")

        schema = [
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("kicker", "STRING"),
            bigquery.SchemaField("link", "STRING"),
            bigquery.SchemaField("image_url", "STRING"),
            bigquery.SchemaField("title_word_count", "INTEGER"),
            bigquery.SchemaField("title_char_count", "INTEGER"),
            bigquery.SchemaField("capitalized_words", "STRING", mode="REPEATED"),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print("Tabla creada correctamente.")

def upload_to_bigquery(df: pd.DataFrame):
    """
    Carga un DataFrame en BigQuery, creando dataset y tabla si no existen.
    """

    if not PROJECT_ID or not DATASET_ID or not TABLE_ID:
        raise ValueError("Faltan variables de entorno: PROJECT_ID, DATASET_ID o TABLE_ID")

    full_table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    client = bigquery.Client(project=PROJECT_ID)

    ensure_dataset(client)
    ensure_table(client)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=False
    )

    job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
    job.result()
    print(f"{df.shape[0]} filas cargadas en {full_table_id}.")



def run_get_query(query: str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL en BigQuery y devuelve un DataFrame con los resultados.

    Args:
        query (str): Consulta SQL válida.

    Returns:
        pd.DataFrame: Resultados de la consulta.
    """
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()
    df = results.to_dataframe()
    return df


def test_connection():
    client = bigquery.Client()
    query = 'SELECT "Hello from BigQuery" AS message'
   
    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        print(row.message)