import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # GCP
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    GCP_REGION = os.getenv('GCP_REGION', 'us-central1')
    
    # Ports
    LEGACY_PORT = int(os.getenv('LEGACY_SYSTEM_PORT', 5000))
    CLOUD_PORT = int(os.getenv('CLOUD_SERVICE_PORT', 5001))
    PROXY_PORT = int(os.getenv('PROXY_PORT', 8000))
    
    # Environment
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Features
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    MOCK_DATA = os.getenv('MOCK_DATA', 'true').lower() == 'true'

config = Config()