# This file checks to see if a youtuber has uploaded a video then notifies user when one is uploaded
from googleapiclient.discovery import build
import os
import datetime
import time
from dotenv import load_dotenv
from fetcher import get_channel_id

# Set up notification class 
class Noti:
    def __init__(self, api_key, channel_ids):
        self.api_key = api_key
        self.channel_ids = channel_ids
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.vid_cache = {} 
    
    # Get latest video information
    def get_latest_video(self, channel_id):
        # Set up cache to avoid excession API calls
        if channel_id in self.vid_cache:
            return self.vid_cache[channel_id]

        # fetch channel details using YouTube API
        response = self.youtube.search().list(
            channelId=channel_id,
            order='date',
            part='snippet',
            maxResults=1
        ).execute()

        latest_vid_info = response['items'][0]['snippet']
        self.vid_cache[channel_id] = latest_vid_info
        return latest_vid_info

    def check_new_videos(self):
        # Loop through channel IDs and look for new videos
        for channel_id in self.channel_ids:
            vid_info = self.get_latest_video(channel_id)
            vid_title = vid_info['title']
            vid_published_at = vid_info['publishedAt']

            published_time = datetime.datetime.strptime(vid_published_at, '%Y-%m-%dT%H:%M:%SZ')

            # Check to see if a vide was uploaded within the last minute
            if published_time > datetime.datetime.utcnow() - datetime.timedelta(minutes=1):
                # Check if the 'id' key exists in the video_info dictionary before accessing 'videoId'
                if 'id' in vid_info and 'videoId' in vid_info['id']:
                    vid_link = f'https://www.youtube.com/watch?v={vid_info["id"]["videoId"]}' # Create video link
                    self.send_notification(vid_title, vid_link)
                else:
                    print(f'Error: Video link not found for video "{vid_title}"')
                    print('---')
            
    def send_notification(self, vid_title, vid_link):
        # Show notification for new video
        print(f'New video uploaded: {video_title}')
        print(f'Link: {vid_link}')
        print(f'---')

if __name__ == '__main__':
    load_dotenv()

    # Pass in API key
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    # List of channel ids to be notified about
    channel_ids = get_channel_id([
        'CHANNEL_1',
        'CHANNEL_2',
        'CHANNEL_3'
     ])

    vid_link = None

    # Create Noti object
    noti = Noti(api_key, channel_ids)

    try:
        # Infinite loop to check video every minute
        while True:
            noti.check_new_videos() # Method to check new videos
            time.sleep(60) # Check again every minute

            if vid_link == None:
                print ("No new video found")

    except KeyboardInterrupt:
        # If Ctrl+C is pressed, stop the loop and print a message
        print("YouTube notifier has been stopped.")

    

