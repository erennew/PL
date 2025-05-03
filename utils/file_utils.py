import os
import shutil
import time
import asyncio
from pathlib import Path
from config import DOWNLOADS_DIR, ENCODED_DIR, THUMBNAILS_DIR, WATERMARKS_DIR

async def cleanup_temp_files():
    """Enhanced cleanup with better resource management"""
    while True:
        await asyncio.sleep(3600)  # Run hourly
        try:
            now = time.time()
            for folder in [DOWNLOADS_DIR, ENCODED_DIR, THUMBNAILS_DIR, WATERMARKS_DIR]:
                if not folder.exists():
                    continue

                for item in folder.iterdir():
                    try:
                        # Delete files older than 24 hours
                        if item.is_file() and now - item.stat().st_mtime > 86400:
                            item.unlink()
                        # Delete empty directories older than 1 hour
                        elif item.is_dir() and now - item.stat().st_mtime > 3600:
                            try:
                                item.rmdir()
                            except OSError:  # Directory not empty
                                pass
                    except Exception as e:
                        logger.warning(f"Cleanup failed for {item}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}", exc_info=True)

def get_human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"
