from pyrogram.types import Message
from utils.progress_utils import user_sessions, active_tasks

async def cancel_handler(client, message: Message):
    """Handle cancel command"""
    chat_id = message.chat.id
    if chat_id in active_tasks:
        active_tasks[chat_id].cancel()
        await message.reply("⏹️ Current task cancelled successfully!")
    else:
        await message.reply("❌ No active task to cancel")

async def status_handler(client, message: Message):
    """Show current status"""
    chat_id = message.chat.id
    if chat_id in user_sessions:
        status = user_sessions[chat_id].get("status", "unknown")
        await message.reply(f"🔄 Current status: {status.capitalize()}")
    else:
        await message.reply("ℹ️ No active session")

async def help_handler(client, message: Message):
    """Show help message"""
    await message.reply(
        "🆘 **Help Guide**\n\n"
        "1. Send /magnet with a magnet link to start\n"
        "2. Configure your encoding settings\n"
        "3. Start the processing\n\n"
        "Commands:\n"
        "/start - Show welcome message\n"
        "/magnet - Start with a magnet link\n"
        "/cancel - Cancel current operation\n"
        "/status - Show current status\n"
        "/help - Show this message"
    )
