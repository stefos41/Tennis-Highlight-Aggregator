import yt_dlp
from yt_dlp.utils import DownloadError

def get_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return None
                
            video = info.get('entries', [info])[0] if info else None
            if not video:
                return None
                
            return {
                'video_id': video.get('id'),
                'title': video.get('title', 'No Title'),
                'channel': video.get('uploader', 'Unknown Channel'),
                'duration': video.get('duration', 0),
                'view_count': video.get('view_count', 0),
            }
            
    except Exception as e:
        print(f"Error extracting video info: {str(e)}")
        return None