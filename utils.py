import asyncio
import time
import logging
import humanize
from datetime import datetime
from typing import Dict, Optional, Tuple
from pyrogram import Client
from pyrogram.errors import FloodWait

logger = logging.getLogger(__name__)

class FloodControl:
    def __init__(self):
        self.last_request = {}
        self.wait_times = {}

    async def wait_if_needed(self, chat_id: int):
        now = time.time()
        if chat_id in self.wait_times and now < self.wait_times[chat_id]:
            await asyncio.sleep(self.wait_times[chat_id] - now)
        
        if chat_id in self.last_request:
            elapsed = now - self.last_request[chat_id]
            if elapsed < 2:
                wait = min(60, 2 ** (int(elapsed) + 1))
                self.wait_times[chat_id] = now + wait
                await asyncio.sleep(wait)
        
        self.last_request[chat_id] = now

flood_control = FloodControl()

async def update_progress(
    client: Client,
    chat_id: int,
    text: str,
    progress: Optional[float] = None,
    force_new: bool = False,
    last_msg_id: Optional[int] = None
) -> int:
    """Update progress message with flood control"""
    try:
        await flood_control.wait_if_needed(chat_id)
        
        if progress is not None:
            progress_bar = "[" + "⬜" * int(progress/10) + "🟪" * (10-int(progress/10)) + f"] {progress:.1f}%"
            text = f"{text}\n\n{progress_bar}"
        
        text += f"\n\n🕒 {datetime.now().strftime('%H:%M:%S')}"
        
        if last_msg_id and not force_new:
            try:
                await client.edit_message_text(chat_id, last_msg_id, text)
                return last_msg_id
            except:
                pass
                
        msg = await client.send_message(chat_id, text)
        return msg.id
        
    except Exception as e:
        logger.error(f"Progress update failed: {e}")
        return last_msg_id or 0

async def cleanup_files():
    """Cleanup old temporary files"""
    while True:
        await asyncio.sleep(3600)
        try:
            now = time.time()
            for folder in ["downloads", "encoded", "thumbnails", "watermarks"]:
                for item in os.listdir(folder):
                    item_path = os.path.join(folder, item)
                    try:
                        if os.path.isfile(item_path) and now - os.path.getmtime(item_path) > 86400:
                            os.remove(item_path)
                    except:
                        continue
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
