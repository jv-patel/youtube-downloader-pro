import os
import tempfile
import yt_dlp
import humanfriendly


class YouTubeDownloader:
    def __init__(self):
        self.base_options = {
            "quiet": True,
            "no_warnings": True,
        }

    def get_video_info(self, url):
        options = self.base_options.copy()

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []

        for fmt in info.get("formats", []):
            if fmt.get("vcodec") != "none":
                formats.append({
                    "quality": fmt.get("format_note") or f"{fmt.get('height', '?')}p",
                    "format_id": fmt["format_id"],
                    "extension": fmt.get("ext", "mp4")
                })

        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "thumbnail": info.get("thumbnail"),
            "duration": humanfriendly.format_timespan(info.get("duration", 0)),
            "views": info.get("view_count", 0),
            "likes": info.get("like_count", "Hidden"),
            "formats": formats,
        }

    def download_video(self, url, format_id):
        temp_dir = tempfile.mkdtemp()

        options = {
            "format": format_id,
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return filename

    def download_audio(self, url):
        temp_dir = tempfile.mkdtemp()

        options = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = os.path.splitext(
                ydl.prepare_filename(info)
            )[0] + ".mp3"

        return filename
