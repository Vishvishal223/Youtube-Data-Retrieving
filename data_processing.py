import pandas as pd

def data_to_dataframe(channel_data, video_data):
    
    try:
        
        if not channel_data or not isinstance(channel_data, dict):
            raise ValueError("Invalid or empty channel data provided.")

        if not video_data or not isinstance(video_data, list):
            raise ValueError("Invalid or empty video data provided.")

        
        channel_df = pd.DataFrame([channel_data])
        
        
        for video in video_data:
            video['channel_id'] = channel_data['channel_id']
        
        video_df = pd.DataFrame(video_data)

        
        print("Channel DataFrame shape:", channel_df.shape)
        print("Video DataFrame shape:", video_df.shape)
        print("Channel DataFrame head:", channel_df.head())
        print("Video DataFrame head:", video_df.head())

        return channel_df, video_df

    except Exception as e:
        print(f"An error occurred while converting data to DataFrame: {e}")
        return None, None
