import asyncio
import logging
from pyrogram import Client
from config import LOGS_DIR, API_ID, API_HASH, BOT_TOKEN
from handlers import register_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "encoder_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    bot = None
    try:
        # Initialize bot
        bot = Client(
            "video_encoder_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100,
            max_concurrent_transmissions=5
        )
        
        # Register handlers
        register_handlers(bot)
        
        logger.info("Starting bot...")
        await bot.start()
        print("Bot is running! Press Ctrl+C to stop")
        await asyncio.Event().wait()  # Run forever
        
    except Exception as e:
        logger.critical(f"Bot crashed: {str(e)}", exc_info=True)
    finally:
        if bot:
            logger.info("Stopping bot...")
            await bot.stop()
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
