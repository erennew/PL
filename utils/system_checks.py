import asyncio
import logging
from config import FFMPEG_CMD, FFPROBE_CMD

logger = logging.getLogger(__name__)

async def check_system_requirements():
    """Verify all required tools are available"""
    required = [FFMPEG_CMD, FFPROBE_CMD]
    missing = []

    for cmd in required:
        try:
            process = await asyncio.create_subprocess_exec(
                cmd, '-version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.wait()
            if process.returncode != 0:
                missing.append(cmd)
        except:
            missing.append(cmd)

    if missing:
        raise RuntimeError(f"Missing required tools: {', '.join(missing)}")
    
    logger.info("System requirements check passed")
