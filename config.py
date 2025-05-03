import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
API_ID = int(os.getenv("API_ID", 24500584))
API_HASH = os.getenv("API_HASH", "449da69cf4081dc2cc74eea828d0c490")
BOT_TOKEN = os.getenv("BOT_TOKEN", "1599848664:AAHc75il2BECWK39tiPv4pVf-gZdPt4MFcw")

# System limits
MAX_CONCURRENT_TASKS = 3
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
MAX_TORRENT_SIZE = 5 * 1024 * 1024 * 1024  # 5GB

# Directory setup
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
ENCODED_DIR = BASE_DIR / "encoded"
THUMBNAILS_DIR = BASE_DIR / "thumbnails"
WATERMARKS_DIR = BASE_DIR / "watermarks"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"

# Create directories if they don't exist
for directory in [DOWNLOADS_DIR, ENCODED_DIR, THUMBNAILS_DIR, WATERMARKS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Quality presets
QUALITY_PRESETS = {
    '480p': {'height': 480, 'crf': 23, 'preset': 'fast', 'bitrate': '1000k'},
    '720p': {'height': 720, 'crf': 21, 'preset': 'medium', 'bitrate': '2500k'},
    '1080p': {'height': 1080, 'crf': 20, 'preset': 'slow', 'bitrate': '5000k'},
    'original': {'height': None, 'crf': None, 'preset': None, 'bitrate': None}
}

# Default settings
DEFAULT_SETTINGS = {
    'quality': '720p',
    'upload_mode': 'video',
    'watermark': str(ASSETS_DIR / "default_wm.png"),
    'thumbnail': str(ASSETS_DIR / "default_thumb.jpg"),
    'metadata': {'title': 'Untitled'}
}

# FFmpeg configuration
FFMPEG_CMD = "ffmpeg"
FFPROBE_CMD = "ffprobe"
