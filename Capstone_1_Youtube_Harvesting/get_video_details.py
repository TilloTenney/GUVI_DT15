from googleapiclient.discovery import build
import isodate as iso

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "Api_Key"
youtube = build('youtube', 'v3', developerKey=api_key)



# FUNCTION TO GET VIDEO DETAILS
def get_video_details(v_ids):
    video_stats = []

    for i in range(0, len(v_ids), 50):
        response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(v_ids[i:i + 50])).execute()
        for video in response['items']:
            dur = iso.parse_duration(video['contentDetails']['duration'])
            date = iso.parse_date(video['snippet']['publishedAt'])
            video_details = dict(Channel_name=video['snippet']['channelTitle'],
                                 Channel_id=video['snippet']['channelId'],
                                 Video_id=video['id'],
                                 Title=video['snippet']['title'],
                                 Tags=video['snippet'].get('tags'),
                                 Thumbnail=video['snippet']['thumbnails']['default']['url'],
                                 Description=video['snippet']['description'],
                                 Published_date=video['snippet']['publishedAt'],
                                 Duration=dur.total_seconds(),
                                 Views=video['statistics']['viewCount'],
                                 Likes=video['statistics'].get('likeCount'),
                                 DisLikes=video['statistics'].get('dislikeCount'),
                                 Comments=video['statistics'].get('commentCount'),
                                 Favorite_count=video['statistics']['favoriteCount'],
                                 Definition=video['contentDetails']['definition'],
                                 Caption_status=video['contentDetails']['caption']
                                 )
            video_stats.append(video_details)
    return video_stats
