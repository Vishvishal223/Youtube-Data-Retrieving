import streamlit as st
from youtube_data import get_youtube_data
from data_processing import data_to_dataframe
from database_manager import migrate_data_to_sql
from query_executor import execute_query
import pandas as pd

# YouTube API key
API_KEY = 'AIzaSyAG7QUIbSUV0bORwfqjG4kiRVdpB_tQ7lc'

st.title("Youtube Data Retreving")

# Input for YouTube Channel ID
channel_id_input = st.text_input("Enter YouTube Channel ID:")

if st.button("Fetch Data"):
    if channel_id_input:
        st.write("Fetching data for channel ID:", channel_id_input)
        
        channel_data, video_data = get_youtube_data(API_KEY, channel_id_input)
        
        if channel_data and video_data:
            
            channel_df, video_df = data_to_dataframe(channel_data, video_data)
            
            
            st.session_state.channel_df = channel_df
            st.session_state.video_df = video_df
            
            st.write("**Channel DataFrame:**")
            st.write(channel_df)
            
            st.write("**Video DataFrame:**")
            st.write(video_df)
            
            st.subheader("Channel Details")
            st.write(channel_df)
            
            st.subheader("Video Details")
            st.write(video_df)
            
            st.write("Ready to migrate data. Click the button below.")
        else:
            st.error("No data found for the given channel ID.")
    else:
        st.error("Please enter a YouTube Channel ID.")

# Migration to SQL
if st.button("Migrate Data to SQL"):
    if 'channel_df' in st.session_state and 'video_df' in st.session_state:
        channel_df = st.session_state.channel_df
        video_df = st.session_state.video_df
        st.write("Migrate Data to SQL button clicked!")
        result = migrate_data_to_sql(channel_df, video_df)
        st.write(result)
    else:
        st.error("Data not found. Please fetch data first.")


st.subheader("SQL Queries")

if st.button("Show All Videos and Corresponding Channels"):
    query = """
    

    SELECT videos.title AS video_title, 
        SUM(CAST(videos.like_count AS UNSIGNED)) AS total_likes, 
        SUM(CAST(videos.dislike_count AS UNSIGNED)) AS total_dislikes
        FROM videos
        GROUP BY videos.title;

    """
    result_df = execute_query(query)
    if isinstance(result_df, pd.DataFrame):
        st.write(result_df)
    else:
        st.error(result_df)

