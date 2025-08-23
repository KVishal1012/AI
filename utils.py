
# Instructions:
# Before running your notebook, set the following environment variables in your terminal:
#   export SERVICE_ACCOUNT_KEY='<base64-encoded-service-account-json>'
#   export PROJECT_ID='<your-gcp-project-id>'
# You can generate the base64 string using:
#   base64 -i /path/to/service-account.json

import os
from dotenv import load_dotenv
import json
import base64
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

def authenticate():
    
    #Load .env
    load_dotenv()

    SERVICE_ACCOUNT_KEY_STRING_B64 = os.getenv('SERVICE_ACCOUNT_KEY')
    if not SERVICE_ACCOUNT_KEY_STRING_B64:
        # Try to read from .env file
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('SERVICE_ACCOUNT_KEY='):
                        SERVICE_ACCOUNT_KEY_STRING_B64 = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break
        except Exception:
            pass
    if not SERVICE_ACCOUNT_KEY_STRING_B64:
        raise EnvironmentError(
            "SERVICE_ACCOUNT_KEY environment variable is not set and not found in .env file.\n"
            "Set it in your notebook, terminal, or .env file as SERVICE_ACCOUNT_KEY='<base64-encoded-service-account-json>'")
    SERVICE_ACCOUNT_KEY_STRING_B64 = SERVICE_ACCOUNT_KEY_STRING_B64.strip()
    try:
        SERVICE_ACCOUNT_KEY_BYTES_B64 = SERVICE_ACCOUNT_KEY_STRING_B64.encode("ascii")
        SERVICE_ACCOUNT_KEY_STRING_BYTES = base64.b64decode(SERVICE_ACCOUNT_KEY_BYTES_B64)
        SERVICE_ACCOUNT_KEY_STRING = SERVICE_ACCOUNT_KEY_STRING_BYTES.decode("utf-8")
        SERVICE_ACCOUNT_KEY = json.loads(SERVICE_ACCOUNT_KEY_STRING)
    except Exception as e:
        raise ValueError(f"Failed to decode or parse SERVICE_ACCOUNT_KEY: {e}")


    # Create credentials based on key from service account
    # Make sure your account has the roles listed in the Google Cloud Setup section
    credentials = Credentials.from_service_account_info(
        SERVICE_ACCOUNT_KEY,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    if credentials.expired:
        credentials.refresh(Request())
    
    #Set project ID according to environment variable    
    PROJECT_ID = os.getenv('PROJECT_ID')
    if not PROJECT_ID:
        # Try to read from .env file
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('PROJECT_ID='):
                        PROJECT_ID = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break
        except Exception:
            pass
    if not PROJECT_ID:
        raise EnvironmentError(
            "PROJECT_ID environment variable is not set and not found in .env file.\n"
            "Set it in your notebook, terminal, or .env file as PROJECT_ID='<your-gcp-project-id>'")
        
    return credentials, PROJECT_ID

def init_vertex_ai(project_id, credentials):
    import vertexai
    vertexai.init(project=project_id, location="us-central1", credentials=credentials)
    return vertexai
