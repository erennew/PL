from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from templates.messages import start_message

async def start_handler(client, message: Message):
    """Initialize bot with welcome message"""
    try:
        await message.reply(
            start_message,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📌 Get Started", callback_data="get_started")],
                [InlineKeyboardButton("ℹ️ Help", callback_data="show_help")]
            ])
        )
    except Exception as e:
        logger.error(f"Start handler error: {str(e)}")
        await message.reply("❌ Failed to initialize bot. Please try again.")
