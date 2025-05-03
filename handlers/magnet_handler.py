from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import DEFAULT_SETTINGS
from utils.progress_utils import user_sessions
from utils.torrent_utils import validate_magnet_link
from templates.messages import magnet_help_message

async def magnet_handler(client, message: Message):
    """Handle magnet link command with validation"""
    chat_id = message.chat.id
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        return await message.reply(
            magnet_help_message,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{chat_id}")]
            ])
        )

    magnet_link = args[1].strip()
    if not validate_magnet_link(magnet_link):
        return await message.reply(
            "❌ Invalid magnet link format!\n\n"
            "A valid magnet link should start with `magnet:?` and contain "
            "either an info hash (btih) or a web link.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Try Again", callback_data="retry_magnet")],
                [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{chat_id}")]
            ])
        )

    # Initialize user session with default settings
    user_sessions[chat_id] = {
        **DEFAULT_SETTINGS,
        "magnet_link": magnet_link,
        "status": "configuring",
        "start_time": time.time()
    }
    
    await collect_settings(chat_id)
