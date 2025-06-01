import harperdb
from yt_extractor import get_info
from config import Config



db = harperdb.HarperDB(
    url=Config.DB_URL,
    username=Config.DB_USER,
    password=Config.DB_PASSWORD
)

def validate_highlight_data(data):
    """Ensure data has required fields with proper types"""
    if not data or not isinstance(data, dict):
        return False
        
    required = {
        'video_id': str,
        'title': str,
        'duration': (int, float),
        'channel': str
    }
    
    for field, field_type in required.items():
        if field not in data or not isinstance(data[field], field_type):
            return False
            
    return True

def insert_highlights(highlight_data):
    if not validate_highlight_data(highlight_data):
        raise ValueError("Invalid highlight data format")
        
    try:
        return db.insert(Config.DB_SCHEMA, Config.DB_TABLE, [highlight_data])
    except Exception as e:
        raise Exception(f"Database insert failed: {str(e)}")

def delete_highlight(highlight_id):
    try:
        return db.delete(Config.DB_SCHEMA, Config.DB_TABLE, [highlight_id])
    except Exception as e:
        raise Exception(f"Database delete failed: {str(e)}")

def get_all_highlights():
    try:
        return db.sql(f"select video_id, channel, title, duration from {Config.DB_SCHEMA}.{Config.DB_TABLE}")
    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")

def get_highlight_today():
    try:
        return db.sql(f"select * from {Config.DB_SCHEMA}.{Config.DB_TABLE_TODAY} where id = 0")
    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")

def update_highlight_today(highlight_data, insert=False):
    if not validate_highlight_data(highlight_data):
        raise ValueError("Invalid highlight data format")
        
    highlight_data['id'] = 0
    try:
        if insert:
            return db.insert(Config.DB_SCHEMA, Config.DB_TABLE_TODAY, [highlight_data])
        return db.update(Config.DB_SCHEMA, Config.DB_TABLE_TODAY, [highlight_data])
    except Exception as e:
        raise Exception(f"Database update failed: {str(e)}")