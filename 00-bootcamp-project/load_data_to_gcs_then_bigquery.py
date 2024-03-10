import json
import os

from google.cloud import bigquery, storage
from google.oauth2 import service_account


DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
location = "asia-southeast1"

# Prepare and Load Credentials to Connect to GCP Services
keyfile_gcs = "/workspaces/data-engineering-bootcamp/00-bootcamp-project/dataworkshopday2-deb3-uploading-files-to-gcs-f9233f86727d.json"
service_account_info_gcs = json.load(open(keyfile_gcs))
credentials_gcs = service_account.Credentials.from_service_account_info(
    service_account_info_gcs
)

keyfile_bigquery = "/workspaces/data-engineering-bootcamp/00-bootcamp-project/dataworkshopday2-deb3-load-files-to-bigquery-3c5e0f358c17.json"
service_account_info_bigquery = json.load(open(keyfile_bigquery))
credentials_bigquery = service_account.Credentials.from_service_account_info(
    service_account_info_bigquery
)

project_id = "dataworkshopday2"

# Load data from Local to GCS
bucket_name = "deb3-bootcamp-06"
storage_client = storage.Client(
    project=project_id,
    credentials=credentials_gcs,
)
bucket = storage_client.bucket(bucket_name)

#addresses
data = "addresses"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{data}.csv"

# YOUR CODE HERE TO LOAD DATA TO GCS
for file in os.listdir(DATA_FOLDER):
    data = file.split(".")[0]

    # if data == "events":
    #     dt = "2021-02-10"
    #     partition = dt.replace("-", "")
    #     file_path = f"{DATA_FOLDER}/{data}.csv"
    #     destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{dt}/{data}.csv"

    destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{data}.csv"
    file_path = f"{DATA_FOLDER}/{data}.csv"

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

# Load data from GCS to BigQuery
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials_bigquery,
        location=location,
    )
    table_id = f"{project_id}.deb_bootcamp.{data}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )
    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=location,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")