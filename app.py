import random
import streamlit as st
from yt_extractor import get_info
import database_service as dbs
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_resource
def get_highlights():
    try:
        return dbs.get_all_highlights()
    except Exception as e:
        logger.error(f"Error fetching highlights: {str(e)}")
        st.error("Failed to load highlights from database")
        return []

def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text

def main():
    st.title("Tennis Highlight APP")

    menu_options = ("Today's Highlight", "All Highlights", "Add Highlight")
    selection = st.sidebar.selectbox("Menu", menu_options)

    if selection == "All Highlights":
        st.markdown(f"## All Highlights")
        
        highlights = get_highlights()
        if not highlights:
            st.warning("No Highlights in Database!")
            return

        for wo in highlights:
            try:
                url = "https://youtu.be/" + wo["video_id"]
                st.subheader(wo['title'])
                st.caption(f"{wo['channel']} - {get_duration_text(wo['duration'])}")
                
                if st.button('Delete Highlight', key=wo["video_id"]):
                    try:
                        dbs.delete_highlight(wo["video_id"])
                        st.cache_resource.clear()
                        st.success("Highlight deleted successfully!")
                        st.experimental_rerun()
                    except Exception as e:
                        logger.error(f"Error deleting highlight: {str(e)}")
                        st.error("Failed to delete highlight")
                
                st.video(url)
            except Exception as e:
                logger.error(f"Error displaying highlight {wo.get('video_id')}: {str(e)}")
                continue

    elif selection == "Add Highlight":
        st.markdown(f"## Add Highlight")
        
        url = st.text_input('Enter YouTube video URL')
        if url:
            try:
                highlight_data = get_info(url)
                if highlight_data is None:
                    st.error("Could not find video information")
                else:
                    st.subheader(highlight_data['title'])
                    st.caption(highlight_data['channel'])
                    st.video(url)
                    
                    if st.button("Add Highlight"):
                        try:
                            dbs.insert_highlights(highlight_data)
                            st.cache_resource.clear()
                            st.success("Highlight added successfully!")
                        except ValueError as e:
                            st.error(f"Invalid data: {str(e)}")
                        except Exception as e:
                            logger.error(f"Error adding highlight: {str(e)}")
                            st.error("Failed to add highlight to database")
            except Exception as e:
                logger.error(f"Error processing URL {url}: {str(e)}")
                st.error("Failed to process video URL")

    else:  # Today's Highlight
        st.markdown(f"## Today's Highlight")
        
        highlights = get_highlights()
        if not highlights:
            st.warning("No Highlights in Database!")
            return

        try:
            wo = dbs.get_highlight_today()
            
            if not wo or wo[0] not in highlights:
                # Select random highlight if none is set for today
                n = len(highlights)
                idx = random.randint(0, n-1)
                wo = highlights[idx]
                try:
                    dbs.update_highlight_today(wo, insert=True)
                except Exception as e:
                    logger.error(f"Error setting today's highlight: {str(e)}")
                    st.error("Failed to set today's highlight")
            else:
                wo = wo[0]
            
            if st.button("Choose another Highlight"):
                n = len(highlights)
                if n > 0:
                    idx = random.randint(0, n-1)
                    wo_new = highlights[idx]
                    while wo_new['video_id'] == wo['video_id'] and n > 1:
                        highlights_new = [w for w in highlights if w['video_id'] != wo['video_id']]
                        idx = random.randint(0, len(highlights_new)-1)
                        wo_new = highlights_new[idx]
                    wo = wo_new
                    try:
                        dbs.update_highlight_today(wo)
                        st.experimental_rerun()
                    except Exception as e:
                        logger.error(f"Error updating today's highlight: {str(e)}")
                        st.error("Failed to update today's highlight")
            
            url = "https://youtu.be/" + wo["video_id"]
            st.subheader(wo['title'])
            st.caption(f"{wo['channel']} - {get_duration_text(wo['duration'])}")
            st.video(url)
            
        except Exception as e:
            logger.error(f"Error displaying today's highlight: {str(e)}")
            st.error("Failed to load today's highlight")

if __name__ == "__main__":
    main()