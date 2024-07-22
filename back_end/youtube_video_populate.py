from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import os
from dotenv import load_dotenv
import time

# Load environment variables from a .env file (optional)
load_dotenv()

# Retrieve the Google API Key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

def youtube_video_populate(channel_id):
    """
    Retrieve video details and statistics from a specified YouTube channel
    and return the data in a pandas DataFrame.

    Args:
    - channel_id (str): The YouTube channel ID.

    Returns:
    - pd.DataFrame: DataFrame containing video_id, title, published_date, view_count, like_count.
    """
    # Build the YouTube service object
    youtube = build('youtube', 'v3', developerKey=api_key)

    def make_api_request(request):
        """
        Make an API request and handle quota errors with exponential backoff.
        """
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = request.execute()
                return response
            except HttpError as e:
                if e.resp.status in [403, 429]:  # Quota exceeded or rate limit exceeded
                    retry_count += 1
                    sleep_time = 2 ** retry_count  # Exponential backoff
                    print(f"Quota exceeded. Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    raise  # Re-raise the exception if it's not a quota error
        raise Exception("Max retries exceeded. Quota still exceeded.")

    video_details = []

    # Get video IDs
    request = youtube.search().list(
        channelId=channel_id,
        part='id,snippet',
        maxResults=50,
        order='date'
    )

    while request:
        response = make_api_request(request)
        video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']

        if not video_ids:
            break

        # Get video statistics for each video ID
        stats_request = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,statistics'
        )
        stats_response = make_api_request(stats_request)

        for item in stats_response['items']:
            video_id = item['id']
            video_title = item['snippet']['title']
            publish_date = item['snippet']['publishedAt']
            view_count = item['statistics'].get('viewCount', 0)
            like_count = item['statistics'].get('likeCount', 0)

            # Exclude shorts (videos less than 60 seconds long) if possible
            if item['snippet'].get('categoryId', '') != '22' or int(
                    item['contentDetails'].get('duration', 'PT0S')[2:-1]) >= 60:
                video_details.append({
                    'video_id': video_id,
                    'title': video_title,
                    'published_date': publish_date,
                    'view_count': view_count,
                    'like_count': like_count
                })

        request = youtube.search().list_next(request, response)

    # Convert to DataFrame
    full_channel_df = pd.DataFrame(video_details)
    return full_channel_df

# Kutzgesagt channel_id = UCsXVk37bltHxD1rDPwtNM8Q
# 238 videos
if __name__ == '__main__':
    for_csv_df = youtube_video_populate(channel_id='UCsXVk37bltHxD1rDPwtNM8Q')
    for_csv_df.to_csv('test_data/youtube_video_populated.csv', index=False, sep='~')