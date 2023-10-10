from googleapiclient.discovery import build

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "Api_Key"
youtube = build('youtube', 'v3', developerKey=api_key)


# FUNCTION TO GET PLAYLIST DETAILS
def get_playlist_name(channel_id):
    playlist_name = []
    for j in range(len(channel_id)):
        request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id[j],
        maxResults=500
        )
        response = request.execute()
        for i in range(len(response['items'])):
            data = dict(Playlist_id=response['items'][i]['id'],
                    Channel_id=channel_id[j],
                    Playlist_name=response['items'][i]['snippet']['title'],
                    Channel_name=response['items'][i]['snippet']['channelTitle'])
            playlist_name.append(data)
        #print(playlist_name)
    return playlist_name
