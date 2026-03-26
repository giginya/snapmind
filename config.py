# config.py

import os

# APP
APP_NAME = "SnapMind"
DEBUG = True

# STORAGE
LOCAL_DB_PATH = "snapmind/storage/local/db.json"
QUEUE_PATH = "snapmind/storage/cloud/queue.json"

# ML
MODEL_PATH = "snapmind/ml/model.pkl"
FEEDBACK_PATH = "snapmind/ml/data/feedback.json"

# CLOUD
GOOGLE_CREDENTIALS = "snapmind/config/credentials.json"
SHEET_NAME = "SnapMindDB"

# LIMITS
MAX_FILE_SIZE_MB = 5
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]
