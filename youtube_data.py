from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_youtube_data(api_key, channel_id):
    try:
        
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        
        channel_request = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        )
        channel_response = channel_request.execute()
        
        if not channel_response['items']:
            return None, None  
        
        
        playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        if not playlist_id:
            return None, None  
        
        
        video_ids = []
        next_page_token = None
        
        while True:
            playlist_request = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            
            for item in playlist_response['items']:
                video_ids.append(item['snippet']['resourceId']['videoId'])
            
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
        
        if not video_ids:
            return channel_data, []  

        
        videos_request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(video_ids)
        )
        videos_response = videos_request.execute()

        
        channel_data = {
            'channel_name': channel_response['items'][0]['snippet']['title'],
            'channel_id': channel_id,
            'subscribers': channel_response['items'][0]['statistics'].get('subscriberCount', 0),
            'total_views': channel_response['items'][0]['statistics'].get('viewCount', 0),
            'total_videos': channel_response['items'][0]['statistics'].get('videoCount', 0)
        }
        
        video_data = []
        for item in videos_response['items']:
            video_data.append({
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': item['statistics'].get('viewCount', 0),
                'like_count': item['statistics'].get('likeCount', 0),
                'dislike_count': item['statistics'].get('dislikeCount', 0),
                'comment_count': item['statistics'].get('commentCount', 0),
                'duration': item['contentDetails']['duration']
            })
        
        return channel_data, video_data
    
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
