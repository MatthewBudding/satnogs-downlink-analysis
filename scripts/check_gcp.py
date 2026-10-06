import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.cloud import storage


def main():
    # 1. Load variables from .env into the environment
    load_dotenv()

    # 2. Read GCP_PROJECT_ID and GCS_BUCKET from the environment
    project_id = os.getenv("GCP_PROJECT_ID")
    gcs_bucket = os.getenv("GCS_BUCKET")

    # 3. If either is None, print a helpful message and exit
    if not project_id or not gcs_bucket:
        raise ValueError("Couldn't find GCP_PROJECT_ID or GCS_BUCKET in .env")
    # 4. Create a storage client for your project
    #    -> storage.Client(project=...)
    client = storage.Client(project=project_id)

    # 5. Get a reference to your bucket (no network call yet)
    #    -> client.bucket(bucket_name)
    bucket = client.bucket(gcs_bucket)
    # 6. Get a reference to a blob named "setup-check/hello.txt"
    #    -> bucket.blob("...")
    blob = bucket.blob("setup-check/hello.txt")

    # 7. Build a message string that includes the current UTC time
    #    -> datetime.now(timezone.utc).isoformat() gives a timestamp string
    message = datetime.now(timezone.utc).isoformat()
    # 8. Upload the message (network call)
    #    -> blob.upload_from_string(message)
    blob.upload_from_string(message)
    # 9. List everything in the bucket and print each name and size
    #    -> client.list_blobs(bucket_name) returns an iterable of blobs
    #    -> each blob has .name and .size attributes
    blobs = client.list_blobs(gcs_bucket)
    for blob_item in blobs:
        print(blob_item.name, blob_item.size)
    # 10. Delete the test blob (network call)
    #     -> blob.delete()
    blob.delete()
    # 11. Print a final success message
    print("Finished")


if __name__ == "__main__":
    main()
