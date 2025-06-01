from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import yt_dlp
import harperdb
import logging
from typing import Optional

# Initialize FastAPI with metadata
app = FastAPI(
    title="Tennis Highlights API",
    description="API for managing tennis highlight videos",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBasic()

# HarperDB Configuration
HARPERDB_URL = "" #add your own harperdb cloud database url
HARPERDB_USERNAME = "" #add your own user for the harperdb cloud databse
HARPERDB_PASSWORD = "" #add your own password for the harperdb cloud database

db = harperdb.HarperDB(
    url=HARPERDB_URL,
    username=HARPERDB_USERNAME,
    password=HARPERDB_PASSWORD
)

SCHEMA = "highlight_repo"
TABLE = "highlights"
TABLE_TODAY = "highlight_today"

# API Key configuration
API_KEYS = {
    "tennis-ext-123": "valid-key"
}

async def verify_api_key(api_key: str = Header(...)):
    """Verify the API key in request headers"""
    if api_key not in API_KEYS.values():
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return api_key

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Root endpoint that returns HTML documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tennis Highlights API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
                color: #333;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            .endpoint {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 15px;
                border-left: 4px solid #3498db;
            }
            .method {
                display: inline-block;
                padding: 3px 8px;
                background-color: #3498db;
                color: white;
                border-radius: 3px;
                font-weight: bold;
                margin-right: 10px;
            }
            code {
                background-color: #f0f0f0;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: monospace;
            }
            a {
                color: #2980b9;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .links {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>🎾 Tennis Highlights API</h1>
        <p>The API is running successfully. Below are the available endpoints:</p>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/video-info?url=YOUTUBE_URL</code>
            <p>Get information about a YouTube video. Requires <code>api-key</code> header.</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/add-highlight</code>
            <p>Add a new highlight to the database. Requires <code>api-key</code> header and JSON payload.</p>
        </div>
        
        <div class="links">
            <p>Explore the API documentation:</p>
            <ul>
                <li><a href="/docs" target="_blank">📚 Swagger UI</a> - Interactive API documentation</li>
                <li><a href="/redoc" target="_blank">📖 ReDoc</a> - Alternative documentation</li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.get("/video-info", tags=["YouTube"], summary="Get YouTube video information")
async def get_video_info(
    url: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Extract information from a YouTube video URL.
    
    - **url**: YouTube video URL (required)
    - Returns: Video ID, title, channel, duration, and view count
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Try to extract basic info first
            info_dict = ydl.extract_info(url, download=False, process=False)
            if not info_dict:
                raise HTTPException(
                    status_code=404,
                    detail="URL not recognized as YouTube video"
                )
                
            # Handle playlists or single videos
            if 'entries' in info_dict:
                info_dict = ydl.extract_info(url, download=False)
                video = info_dict['entries'][0] if info_dict['entries'] else None
            else:
                video = info_dict
                
            if not video:
                raise HTTPException(
                    status_code=404,
                    detail="No video found at URL"
                )
                
            # Check for various restrictions
            if video.get('is_live'):
                raise HTTPException(
                    status_code=400,
                    detail="Live streams not supported"
                )
            if video.get('age_limit', 0) > 0:
                raise HTTPException(
                    status_code=403,
                    detail="Age-restricted content not supported"
                )
            if video.get('availability') == 'private':
                raise HTTPException(
                    status_code=403,
                    detail="Private video - cannot access"
                )
                
            duration = video.get('duration', 0)
            if duration > 3600:  # 1 hour
                raise HTTPException(
                    status_code=400,
                    detail="Videos longer than 1 hour not supported"
                )
                
            return {
                'video_id': video.get('id'),
                'title': video.get('title', 'No Title'),
                'channel': video.get('uploader', 'Unknown Channel'),
                'duration': duration,
                'view_count': video.get('view_count', 0),
                'thumbnail': video.get('thumbnail'),
            }
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        if 'private video' in error_msg:
            detail = "Private video - cannot access"
        elif 'unavailable' in error_msg:
            detail = "Video unavailable"
        elif 'age restricted' in error_msg:
            detail = "Age-restricted content not supported"
        else:
            detail = f"Could not process video: {str(e)}"
        
        logger.error(f"DownloadError: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=detail
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.post("/add-highlight", tags=["Database"], summary="Add a new highlight")
async def add_highlight(
    video_data: dict,
    api_key: str = Depends(verify_api_key)
):
    """
    Add a new tennis highlight to the database.
    
    - **video_data**: Dictionary containing video information (must include video_id, title, and duration)
    - Returns: Success status and database result
    """
    required_fields = ['video_id', 'title', 'duration']
    if not all(field in video_data for field in required_fields):
        raise HTTPException(
            status_code=400,
            detail="Missing required fields (video_id, title, duration)"
        )
    
    try:
        # Additional validation
        if not isinstance(video_data['duration'], (int, float)) or video_data['duration'] <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid duration (must be positive number)"
            )
            
        result = db.insert(SCHEMA, TABLE, [video_data])
        logger.info(f"Added highlight: {video_data['video_id']}")
        return {
            "success": True,
            "result": result,
            "message": "Highlight added successfully"
        }
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",  # Changed to use module import format
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )