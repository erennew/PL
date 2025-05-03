import re
import os
import asyncio
from pathlib import Path
from typing import Dict, Optional, Callable
from config import QUALITY_PRESETS, ENCODED_DIR, FFMPEG_CMD, FFPROBE_CMD

class VideoEncoder:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove special characters from filename"""
        return re.sub(r'[^\w\-_. ]', '', filename)

    @staticmethod
    async def encode_with_progress(
        input_path: str,
        output_path: str,
        quality: str,
        metadata: Dict[str, str],
        watermark_path: Optional[str] = None,
        thumbnail_path: Optional[str] = None,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Convert video with proper progress callback handling"""
        try:
            # Validate input
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Get clean title
            title = metadata.get("title", "Untitled")
            clean_title = VideoEncoder.sanitize_filename(title)
            
            # Build command
            cmd = [FFMPEG_CMD, '-hide_banner', '-loglevel', 'error', '-i', input_path]
            
            # Handle watermark
            if watermark_path and os.path.exists(watermark_path):
                cmd.extend(['-i', watermark_path])
                cmd.extend([
                    '-filter_complex', '[0:v][1:v]overlay=W-w-10:H-h-10[outv]',
                    '-map', '[outv]'
                ])
            else:
                cmd.extend(['-map', '0:v?'])
            
            # Handle quality
            if quality != 'original':
                preset = QUALITY_PRESETS[quality]
                cmd.extend([
                    '-vf', f'scale=-2:{preset["height"]}',
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-crf', str(preset["crf"]),
                    '-preset', preset["preset"],
                    '-b:v', preset["bitrate"]
                ])
            else:
                cmd.extend(['-c:v', 'copy'])
            
            # Handle audio and subtitles
            cmd.extend([
                '-map', '0:a?',
                '-c:a', 'copy',
                '-map', '0:s?',
                '-c:s', 'copy'
            ])
            
            # Add metadata
            metadata_cmds = [
                '-metadata', f'title={clean_title}',
                '-metadata:s:v:0', f'title={clean_title}',
                '-metadata:s:a:0', f'title={clean_title}',
                '-metadata:s:s:0', f'title={clean_title}'
            ]
            cmd.extend(metadata_cmds)
            
            # Set output filename
            output_filename = f"{clean_title}.mkv"
            final_output_path = os.path.join(ENCODED_DIR, output_filename)
            
            cmd.extend([
                '-f', 'matroska',
                '-y',
                final_output_path
            ])
            
            # Execute command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Progress tracking
            start_time = time.time()
            while True:
                if process.returncode is not None:
                    break
                
                if progress_callback:
                    elapsed = time.time() - start_time
                    progress = min(90, elapsed * 1.5)
                    try:
                        await progress_callback(progress)
                    except Exception as e:
                        logger.warning(f"Progress callback error: {str(e)}")
                
                await asyncio.sleep(5)
            
            # Verify completion
            if process.returncode != 0:
                stderr = await process.stderr.read()
                error = stderr.decode('utf-8')[-500:] or "Unknown error"
                raise RuntimeError(f"FFmpeg error: {error}")
            
            if progress_callback:
                await progress_callback(100)
            
            return final_output_path
        
        except Exception as e:
            logger.error(f"Encoding failed: {str(e)}", exc_info=True)
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            raise
