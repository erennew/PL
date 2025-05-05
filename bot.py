import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN, BOT_OWNER_ID
from utils import flood_control, update_progress, cleanup_files
from encoder import VideoEncoder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
sessions = {}
progress_msgs = {}
active_tasks = {}

bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
encoder = VideoEncoder()

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Send /magnet with a link to begin")

@bot.on_message(filters.command("magnet"))
async def magnet(client, message):
    chat_id = message.chat.id
    if len(message.text.split()) < 2:
        return await message.reply("Please provide a magnet link")
        
    magnet = message.text.split()[1]
    sessions[chat_id] = {
        'magnet': magnet,
        'quality': '720p',
        'status': 'ready'
    }
    
    buttons = [
        [InlineKeyboardButton("480p", "qual_480"),
        InlineKeyboardButton("720p", "qual_720")],
        [InlineKeyboardButton("1080p", "qual_1080"),
        InlineKeyboardButton("Original", "qual_orig")]
    ]
    await message.reply("Select quality:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r"^qual_"))
async def quality_callback(client, query):
    chat_id = query.message.chat.id
    quality = {
        'qual_480': '480p',
        'qual_720': '720p',
        'qual_1080': '1080p',
        'qual_orig': 'original'
    }.get(query.data, '720p')
    
    if chat_id in sessions:
        sessions[chat_id]['quality'] = quality
        await query.answer(f"Quality set to {quality}")
        await query.message.edit_text(f"Quality: {quality}\nSend /process to start")
    else:
        await query.answer("Session expired!")

@bot.on_message(filters.command("process"))
async def process(client, message):
    chat_id = message.chat.id
    if chat_id not in sessions:
        return await message.reply("No active session")
        
    session = sessions[chat_id]
    msg_id = await update_progress(client, chat_id, "Starting download...")
    
    async def progress_callback(progress, status):
        await update_progress(client, chat_id, status, progress, False, msg_id)
        
    try:
        # Download and process here using encoder
        # Example:
        # output = await encoder.encode(input, output, session['quality'], {}, None, progress_callback)
        await update_progress(client, chat_id, "Done!", 100, True, msg_id)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update_progress(client, chat_id, f"Failed: {e}", -1, True, msg_id)

@bot.on_message(filters.command("cancel"))
async def cancel(client, message):
    chat_id = message.chat.id
    if chat_id in active_tasks:
        for task in active_tasks[chat_id]:
            task.cancel()
        del active_tasks[chat_id]
    await message.reply("Cancelled all tasks")

if __name__ == "__main__":
    bot.loop.create_task(cleanup_files())
    bot.run()
