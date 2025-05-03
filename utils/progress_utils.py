from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, Optional, List, Tuple
import asyncio
import time
import logging
from config import DOWNLOADS_DIR, ENCODED_DIR, THUMBNAILS_DIR, WATERMARKS_DIR

logger = logging.getLogger(__name__)

# Global session tracker
user_sessions: Dict[int, Dict] = {}
progress_messages: Dict[int, int] = {}
active_tasks: Dict[int, asyncio.Task] = {}

async def update_progress(
    chat_id: int,
    text: str,
    force_new: bool = False,
    message: Optional[Message] = None
) -> Message:
    """Update progress message with proper error handling"""
    try:
        if not force_new and chat_id in progress_messages:
            try:
                msg = await message._client.get_messages(
                    chat_id=chat_id,
                    message_ids=progress_messages[chat_id]
                )
                if msg:
                    return await msg.edit_text(text)
            except:
                pass
        
        msg = await message._client.send_message(
            chat_id=chat_id,
            text=text
        )
        progress_messages[chat_id] = msg.id
        return msg
    except Exception as e:
        logger.error(f"Failed to update progress: {str(e)}")
        raise

async def start_processing(chat_id: int):
    """Handle the complete processing pipeline"""
    try:
        session = user_sessions.get(chat_id)
        if not session or session.get("status") != "downloaded":
            return await update_progress(chat_id, "❌ No downloaded files found", force_new=True)

        file_path = session["file_path"]
        output_dir = ENCODED_DIR / f"batch_{chat_id}_{int(time.time())}"
        output_dir.mkdir(exist_ok=True)
        
        await update_progress(chat_id, "🔄 Starting processing...")

        async def safe_progress_callback(progress: float):
            await update_progress(
                chat_id,
                f"🔧 Processing...\n"
                f"📊 Progress: {progress:.1f}%\n"
                f"🏷️ Title: {session.get('metadata', {}).get('title', '')}"
            )

        try:
            encoded_path = await VideoEncoder.encode_with_progress(
                input_path=file_path,
                output_path=str(output_dir / "temp.mkv"),
                quality=session.get("quality", "720p"),
                metadata=session.get("metadata", {}),
                watermark_path=session.get("watermark"),
                thumbnail_path=session.get("thumbnail"),
                progress_callback=safe_progress_callback
            )
            
            await update_progress(chat_id, "☁️ Starting upload...")
            
            async def upload_progress(current, total):
                progress = (current / total) * 100
                await update_progress(
                    chat_id,
                    f"📤 Uploading...\n"
                    f"📊 Progress: {progress:.1f}%\n"
                    f"🏷️ Title: {session.get('metadata', {}).get('title', '')}"
                )
            
            upload_mode = session.get("upload_mode", "video")
            if upload_mode == "document":
                await message._client.send_document(
                    chat_id=chat_id,
                    document=encoded_path,
                    thumb=session.get("thumbnail"),
                    caption=f"📄 {session.get('metadata', {}).get('title', 'File')}",
                    progress=upload_progress
                )
            else:
                await message._client.send_video(
                    chat_id=chat_id,
                    video=encoded_path,
                    thumb=session.get("thumbnail"),
                    caption=f"🎬 {session.get('metadata', {}).get('title', 'Video')}",
                    progress=upload_progress
                )
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
        
        await update_progress(chat_id, "✅ Processing completed successfully!", force_new=True)
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}", exc_info=True)
        await update_progress(chat_id, f"❌ Processing failed: {str(e)}", force_new=True)
    finally:
        # Cleanup
        try:
            if "encoded_path" in locals() and os.path.exists(encoded_path):
                os.remove(encoded_path)
            if "file_path" in locals() and os.path.exists(file_path):
                os.remove(file_path)
            if "session" in locals() and "download_path" in session:
                shutil.rmtree(session["download_path"], ignore_errors=True)
            if "output_dir" in locals() and os.path.exists(output_dir):
                shutil.rmtree(output_dir, ignore_errors=True)
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")
        
        if chat_id in user_sessions:
            user_sessions.pop(chat_id, None)
        if chat_id in progress_messages:
            progress_messages.pop(chat_id, None)
        if chat_id in active_tasks:
            active_tasks.pop(chat_id, None)
        
