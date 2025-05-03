import re
import logging
from torrentp import TorrentDownloader
from config import DOWNLOADS_DIR, MAX_TORRENT_SIZE

logger = logging.getLogger(__name__)

def validate_magnet_link(magnet: str) -> bool:
    """Validate magnet link format"""
    pattern = r'^magnet:\?xt=urn:btih:[a-zA-Z0-9]+.*$'
    return re.match(pattern, magnet) is not None

async def download_torrent(magnet_link: str, download_path: str) -> str:
    """Download torrent from magnet link"""
    try:
        torrent = TorrentDownloader(magnet_link, download_path)
        torrent.start_download()
        
        while not torrent.is_complete:
            await asyncio.sleep(5)
            progress = torrent.progress
            logger.info(f"Download progress: {progress}%")
            
            if progress >= 100:
                break
        
        if torrent.is_complete:
            # Find the largest video file
            video_files = []
            for root, _, files in os.walk(download_path):
                for file in files:
                    if file.endswith(('.mp4', '.mkv', '.avi', '.mov')):
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        if file_size <= MAX_TORRENT_SIZE:
                            video_files.append((file_path, file_size))
            
            if not video_files:
                raise ValueError("No supported video files found in torrent")
            
            # Return the largest video file
            video_files.sort(key=lambda x: x[1], reverse=True)
            return video_files[0][0]
        else:
            raise Exception("Torrent download incomplete")
    
    except Exception as e:
        logger.error(f"Torrent download failed: {str(e)}")
        raise
