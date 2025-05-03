import asyncio
import logging
from pyrogram import Client
from config import LOGS_DIR, BASE_DIR
from handlers import register_handlers
from utils.system_checks import check_system_requirements
from utils.file_utils import cleanup_temp_files

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
        # Verify system requirements
        await check_system_requirements()
        
        # Start cleanup task
        asyncio.create_task(cleanup_temp_files())
        
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
