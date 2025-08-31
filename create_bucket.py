from google.cloud import storage
from utils import authenticate

credentials, project_id = authenticate()

# Instantiates a client
storage_client = storage.Client(credentials=credentials, project=project_id)

bucket_name = "gen-lang-client-0336314704-bucket"

# Creates the new bucket
bucket = storage_client.create_bucket(bucket_name)

print(f"Bucket {bucket.name} created.")
