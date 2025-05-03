from pyrogram import filters
from .start_handler import start_handler
from .magnet_handler import magnet_handler
from .callback_handlers import (
    quality_set_handler,
    quality_handler,
    set_title_handler,
    set_thumb_handler,
    set_wm_handler,
    confirm_download_handler,
    set_upload_mode_handler
)
from .input_handlers import handle_user_input
from .command_handlers import cancel_handler, status_handler, help_handler

def register_handlers(bot):
    # Command handlers
    bot.on_message(filters.command("start"))(start_handler)
    bot.on_message(filters.command("help"))(help_handler)
    bot.on_message(filters.command("magnet") & filters.private)(magnet_handler)
    bot.on_message(filters.command("cancel") & filters.private)(cancel_handler)
    bot.on_message(filters.command("status") & filters.private)(status_handler)
    
    # Callback handlers
    bot.on_callback_query(filters.regex(r"^set_quality_(\d+)$"))(quality_set_handler)
    bot.on_callback_query(filters.regex(r"^quality_(\w+)_(\d+)$"))(quality_handler)
    bot.on_callback_query(filters.regex(r"^set_title_(\d+)$"))(set_title_handler)
    bot.on_callback_query(filters.regex(r"^set_thumb_(\d+)$"))(set_thumb_handler)
    bot.on_callback_query(filters.regex(r"^set_wm_(\d+)$"))(set_wm_handler)
    bot.on_callback_query(filters.regex(r"^confirm_download_(\d+)$"))(confirm_download_handler)
    bot.on_callback_query(filters.regex(r"^set_upload_(video|doc)_(\d+)$"))(set_upload_mode_handler)
    
    # Input handlers
    bot.on_message(filters.private & (filters.text | filters.photo))(handle_user_input)
