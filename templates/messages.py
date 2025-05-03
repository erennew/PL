start_message = """
🎬 **Welcome to Video Encoder Bot** 🎬

I can help you download and encode videos from magnet links. Here's what I can do:

🔹 Download torrents from magnet links
🔹 Encode videos to different qualities (480p, 720p, 1080p)
🔹 Add watermarks and thumbnails
🔹 Upload as video or document

Send /magnet followed by a magnet link to get started!
"""

magnet_help_message = """
🔗 **How to use magnet links:**

1. Find a torrent with video content
2. Copy the magnet link (should start with `magnet:?`)
3. Send it to me like this:
   `/magnet magnet:?xt=urn:btih:...`

⚠️ Note: I only support video files (mp4, mkv, avi, etc.)
"""

settings_message = """
⚙️ **Encoding Settings**

📊 Quality: **{quality}**
📤 Upload Mode: **{upload_mode}**
🏷 Title: **{title}**
🖼 Thumbnail: **{has_thumbnail}**
💧 Watermark: **{has_watermark}**

Configure your options below:
"""

processing_message = """
🔄 **Processing Your File**

📊 Progress: **{progress}%**
⏳ Elapsed: **{elapsed}**
⏱ ETA: **{eta}**
🏷 Title: **{title}**
"""

error_messages = {
    "invalid_magnet": "❌ Invalid magnet link! Please check and try again.",
    "download_failed": "❌ Download failed! Please check the magnet link.",
    "encoding_failed": "❌ Encoding failed! The file might be corrupted.",
    "upload_failed": "❌ Upload failed! Please try again later."
}
