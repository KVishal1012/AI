from utils import authenticate
import vertexai
from vertexai.preview.tuning import sft

credentials, PROJECT_ID = authenticate()
vertexai.init(project=PROJECT_ID, location="us-east1", credentials=credentials)

tuning_job = sft.train(
    source_model="gemini-1.0-pro",
    train_dataset="gs://gen-lang-client-0336314704-bucket/tune_Data_stack_overflow_python_qa-10:24:08:2025.jsonl",
    tuned_model_display_name="stackoverflow-python-qa-tuned-model",
)

print(f"Tuning job created: {tuning_job.resource_name}")