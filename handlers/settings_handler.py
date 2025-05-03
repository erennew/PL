from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import QUALITY_PRESETS, ASSETS_DIR
from utils.progress_utils import user_sessions
from templates.messages import settings_message

async def collect_settings(chat_id: int):
    """Enhanced settings menu with visual indicators"""
    session = user_sessions.get(chat_id, {})
    
    # Build quality indicator
    quality = session.get("quality", "720p")
    quality_icon = "🟢" if quality != "original" else "🔵"

    # Build upload mode indicator
    upload_mode = session.get("upload_mode", "video")
    upload_icon = "🎥" if upload_mode == "video" else "📄"

    # Build thumbnail status
    thumb_status = "✅" if session.get("thumbnail") else "❌"
    
    # Build watermark status
    wm_status = "✅" if session.get("watermark") else "❌"
    
    # Build title status
    title_status = "✅" if session.get("metadata", {}).get("title") else "❌"

    buttons = [
        [
            InlineKeyboardButton(f"{quality_icon} Quality: {quality}", 
                              callback_data=f"set_quality_{chat_id}"),
            InlineKeyboardButton(f"{title_status} Title", 
                              callback_data=f"set_title_{chat_id}")
        ],
        [
            InlineKeyboardButton(f"{thumb_status} Thumbnail", 
                              callback_data=f"set_thumb_{chat_id}"),
            InlineKeyboardButton(f"{wm_status} Watermark", 
                              callback_data=f"set_wm_{chat_id}")
        ],
        [
            InlineKeyboardButton(
                f"{upload_icon} Upload as {'Video' if upload_mode == 'video' else 'Document'}", 
                callback_data=f"set_upload_{upload_mode}_{chat_id}"
            )
        ],
        [
            InlineKeyboardButton("🚀 Start Processing", 
                              callback_data=f"confirm_download_{chat_id}"),
            InlineKeyboardButton("❌ Cancel", 
                              callback_data=f"cancel_{chat_id}")
        ]
    ]

    await client.send_message(
        chat_id,
        settings_message.format(
            quality=quality,
            upload_mode=upload_mode,
            title=session.get("metadata", {}).get("title", "Not set"),
            has_thumbnail="Yes" if session.get("thumbnail") else "No",
            has_watermark="Yes" if session.get("watermark") else "No"
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
