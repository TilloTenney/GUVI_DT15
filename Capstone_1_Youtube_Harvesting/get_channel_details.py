from googleapiclient.discovery import build

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "Api_Key"
youtube = build('youtube', 'v3', developerKey=api_key)

# FUNCTION TO GET CHANNEL DETAILS
def get_channel_details(channel_id):
    ch_data = []
    for  channel in channel_id:
        request = youtube.channels().list(part='snippet,contentDetails,statistics,status',
                                       id=channel)
        response = request.execute()
        print(response)

        for i in range(len(response['items'])):
            data = dict(Channel_id=channel,
                    Channel_name=response['items'][i]['snippet']['title'],
                    Playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                    Subscribers=response['items'][i]['statistics']['subscriberCount'],
                    Views=response['items'][i]['statistics']['viewCount'],
                    Total_videos=response['items'][i]['statistics']['videoCount'],
                    Description=response['items'][i]['snippet']['description'],
                    Country=response['items'][i]['snippet'].get('country'),
                    Status=response['items'][i]['status']['privacyStatus']
                    #Type=response['items'][i]['status']['madeForKids'] or "Null",
                    )
            ch_data.append(data)
    return ch_data
