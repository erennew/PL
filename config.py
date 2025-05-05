import os
from pathlib import Path

# Bot credentials
API_ID = 24500584
API_HASH = "449da69cf4081dc2cc74eea828d0c490"
BOT_TOKEN = "1599848664:AAHc75il2BECWK39tiPv4pVf-gZdPt4MFcw"

# Limits
MAX_CONCURRENT_TASKS = 3
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
MAX_TOTAL_SIZE = 10 * 1024 * 1024 * 1024  # 10GB

# Paths
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
ENCODED_DIR = BASE_DIR / "encoded"
THUMBNAILS_DIR = BASE_DIR / "thumbnails"
WATERMARKS_DIR = BASE_DIR / "watermarks"

# Create directories
for folder in [DOWNLOADS_DIR, ENCODED_DIR, THUMBNAILS_DIR, WATERMARKS_DIR]:
    folder.mkdir(exist_ok=True)

# Quality presets
QUALITY_PRESETS = {
    '480p': {'height': 480, 'crf': 28, 'bitrate': '1500k'},
    '720p': {'height': 720, 'crf': 27, 'bitrate': '3000k'},
    '1080p': {'height': 1080, 'crf': 26, 'bitrate': '6000k'},
    'original': {'height': -1, 'crf': 18, 'bitrate': '8000k'}
}

# Bot owner
BOT_OWNER_ID = 1047253913
