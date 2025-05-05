import asyncio
import json
import re
from typing import Dict, Optional, Callable
from config import QUALITY_PRESETS

class VideoEncoder:
    def __init__(self):
        self.bitrate = None

    async def encode(
        self,
        input_path: str,
        output_path: str,
        quality: str,
        metadata: Dict,
        watermark: Optional[str] = None,
        progress_cb: Optional[Callable] = None
    ) -> str:
        """Encode video with progress tracking"""
        try:
            duration = await self._get_duration(input_path)
            if duration <= 0:
                raise ValueError("Invalid duration")
                
            cmd = self._build_cmd(input_path, output_path, quality, metadata, watermark, bool(progress_cb))
            process = await asyncio.create_subprocess_exec(*cmd, stderr=asyncio.PIPE)
            
            if progress_cb:
                pattern = re.compile(r"out_time_ms=(\d+)")
                last_progress = 0
                
                while True:
                    line = await process.stderr.readline()
                    if not line:
                        break
                        
                    line = line.decode()
                    if "out_time_ms=" in line:
                        match = pattern.search(line)
                        if match:
                            current = int(match.group(1)) / 1_000_000
                            progress = min(99, (current / duration) * 100)
                            if progress >= last_progress + 1:
                                await progress_cb(progress, "Encoding...")
                                last_progress = progress
                                
            if await process.wait() != 0:
                raise RuntimeError("Encoding failed")
                
            if progress_cb:
                await progress_cb(100, "Done!")
                
            return output_path
        except Exception as e:
            if progress_cb:
                await progress_cb(-1, f"Error: {e}")
            raise

    def _build_cmd(self, input_path, output_path, quality, metadata, watermark, show_progress):
        """Build FFmpeg command"""
        preset = QUALITY_PRESETS.get(quality, QUALITY_PRESETS['720p'])
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error']
        
        if show_progress:
            cmd.extend(['-progress', 'pipe:1', '-nostats'])
            
        cmd.extend(['-i', input_path])
        
        if watermark:
            cmd.extend(['-i', watermark])
            filter_complex = self._get_watermark_filter(preset['height'])
            cmd.extend(['-filter_complex', filter_complex, '-map', '[outv]'])
        elif quality != 'original':
            cmd.extend(['-vf', f"scale=-2:{preset['height']}"])
            
        cmd.extend([
            '-map', '0:a?',
            '-c:v', 'libx264',
            '-crf', str(preset['crf']),
            '-b:v', preset['bitrate'],
            '-preset', 'veryfast',
            '-metadata', f"title={metadata.get('title', '')}",
            '-y', output_path
        ])
        
        return cmd
        
    def _get_watermark_filter(self, height):
        """Generate watermark filter complex"""
        if height > 0:
            return (f"[0:v]scale=-2:{height}[scaled];"
                    f"[1:v]scale=iw*0.05:-1[wm];"
                    f"[scaled][wm]overlay=10:10[outv]")
        return ("[1:v]scale=iw*0.05:-1[wm];"
                "[0:v][wm]overlay=10:10[outv]")
                
    async def _get_duration(self, path):
        """Get video duration using ffprobe"""
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
               '-of', 'default=noprint_wrappers=1:nokey=1', path]
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.PIPE, stderr=asyncio.PIPE)
        stdout, _ = await proc.communicate()
        return float(stdout.decode().strip())
