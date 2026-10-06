from airflow.sdk import dag, task
import os
from datetime import datetime, timezone


@dag(
    schedule=None, #-> only runs when you trigger it manually
    start_date=datetime(2026, 1, 1),
    catchup=False, #-> don't try to run for past dates
    tags=["setup"] #-> optional, helps filter in the UI
)
def gcs_check():

    @task
    def write_file():
        from google.cloud import storage
        # 1. Read GCP_PROJECT_ID and GCS_BUCKET with os.getenv
        #    (no load_dotenv needed: env_file already set them in the container)
        project_id = os.getenv("GCP_PROJECT_ID")
        gcs_bucket = os.getenv("GCS_BUCKET")
        # 2. Create a storage client, bucket, and blob
        #    -> use a different name than your script, like "airflow-check/hello.txt"
        client = storage.Client(project=project_id)
        bucket = client.bucket(gcs_bucket)
        blob = bucket.blob("airflow-check/hello.txt")
        # 3. Upload a message with a timestamp
        message = datetime.now(timezone.utc).isoformat()
        blob.upload_from_string(message)
        # 4. Return the blob name, so the next task knows what to check
        return blob.name
    @task
    def verify_and_delete(blob_name):
        from google.cloud import storage
        # 1. Create a client and bucket again (tasks don't share Python objects)
        project_id = os.getenv("GCP_PROJECT_ID")
        gcs_bucket = os.getenv("GCS_BUCKET")
        client = storage.Client(project=project_id)
        bucket = client.bucket(gcs_bucket)
        # 2. Get the blob by the name passed in
        blob = bucket.blob(blob_name)
        # 3. Read its contents back
        #    -> look up blob.download_as_text()
        content = blob.download_as_text()
        # 4. Print the contents (this shows up in the task's log)
        print(content)
        # 5. Delete the blob
        blob.delete()

    # Wire them together: call write_file(), pass its result into verify_and_delete()
    results = write_file()
    verify_and_delete(results)

gcs_check()
