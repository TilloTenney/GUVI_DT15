from googleapiclient.discovery import build

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "AIzaSyCs0WxXm3TrDBlqdr_eX5ErQ-XJk6kyVwg"
youtube = build('youtube', 'v3', developerKey=api_key)

# FUNCTION TO GET VIDEO IDS
def get_channel_videos(channel_id):
    video_ids = []
    # get Uploads playlist id
    for j in range(len(channel_id)):
        request = youtube.channels().list(id=channel_id[j],
                                  part='contentDetails')
        response = request.execute()
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None

        while True:
            response = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()

            for i in range(len( response['items'])):
                video_ids.append( response['items'][i]['snippet']['resourceId']['videoId'])
                next_page_token =  response.get('nextPageToken')

            if next_page_token is None:
                break
    return video_ids