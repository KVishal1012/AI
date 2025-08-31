from google.cloud import storage
from utils import authenticate

credentials, project_id = authenticate()

# Instantiates a client
storage_client = storage.Client(credentials=credentials, project=project_id)

bucket_name = "gen-lang-client-0336314704-bucket"
bucket = storage_client.bucket(bucket_name)

source_file_name = "eval_Data_stack_overflow_python_qa-10:24:08:2025.jsonl"
destination_blob_name = source_file_name

blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(f"/Users/koushikannamalai/Downloads/Github/AI/AI/{source_file_name}")

print(
    f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}."
)