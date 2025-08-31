from google.cloud import storage
from utils import authenticate

credentials, project_id = authenticate()

# Instantiates a client
storage_client = storage.Client(credentials=credentials)

# Lists all buckets
buckets = storage_client.list_buckets()

print("GCS buckets:")
for bucket in buckets:
    print(bucket.name)