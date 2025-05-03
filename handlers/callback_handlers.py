# handlers/callback_handlers.py
from pyrogram.types import CallbackQuery
from config import QUALITY_PRESETS
from utils.progress_utils import user_sessions

async def quality_set_handler(client, callback_query: CallbackQuery):
    """Handle quality setting selection"""
    chat_id = int(callback_query.data.split("_")[-1])
    await ask_for_quality(chat_id)

async def quality_handler(client, callback_query: CallbackQuery):
    """Handle quality selection"""
    quality = callback_query.data.split("_")[1]
    chat_id = int(callback_query.data.split("_")[-1])
    
    if chat_id not in user_sessions:
        return await callback_query.answer("Session expired!", show_alert=True)

    if quality not in QUALITY_PRESETS:
        return await callback_query.answer("Invalid quality selected!", show_alert=True)

    user_sessions[chat_id]["quality"] = quality
    await callback_query.answer(f"Quality set to {quality}")
    await callback_query.message.edit_text(f"✅ Quality: {quality}")

async def set_title_handler(client, callback_query: CallbackQuery):
    """Prompt for title"""
    chat_id = int(callback_query.data.split("_")[-1])
    await callback_query.answer("Send the title as text")
    user_sessions[chat_id]["awaiting"] = "title"
    await callback_query.message.edit_text("📝 Please send the title as text")

async def set_thumb_handler(client, callback_query: CallbackQuery):
    """Prompt for thumbnail"""
    chat_id = int(callback_query.data.split("_")[-1])
    await callback_query.answer("Send the thumbnail as photo")
    user_sessions[chat_id]["awaiting"] = "thumbnail"
    await callback_query.message.edit_text("🖼️ Please send the thumbnail as photo")

async def set_wm_handler(client, callback_query: CallbackQuery):
    """Prompt for watermark"""
    chat_id = int(callback_query.data.split("_")[-1])
    await callback_query.answer("Send the watermark as photo")
    user_sessions[chat_id]["awaiting"] = "watermark"
    await callback_query.message.edit_text("💧 Please send the watermark as photo")

async def confirm_download_handler(client, callback_query: CallbackQuery):
    """Start download after settings"""
    chat_id = int(callback_query.data.split("_")[-1])
    
    if chat_id not in user_sessions or "magnet_link" not in user_sessions[chat_id]:
        return await callback_query.answer("Session expired!", show_alert=True)

    user_sessions[chat_id]["status"] = "ready_to_download"
    await callback_query.answer("Starting download...")
    await handle_download(chat_id, user_sessions[chat_id]["magnet_link"])

async def set_upload_mode_handler(client, callback_query: CallbackQuery):
    """Set upload mode"""
    mode = callback_query.data.split("_")[2]
    chat_id = int(callback_query.data.split("_")[-1])
    
    if chat_id not in user_sessions:
        return await callback_query.answer("Session expired!", show_alert=True)

    user_sessions[chat_id]["upload_mode"] = mode
    await callback_query.answer(f"✅ Will upload as {mode}")
    await collect_settings(chat_id)
