from dotenv import load_dotenv
import os
import googleapiclient.discovery

# Load environment variables from a .env file (optional)
load_dotenv()

# Retrieve the Google API Key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize the YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)


def youtube_channel_search(channel_name):
    """
    Retrieve the channel ID and other details for a given channel name.

    Args:
    channel_name (str): The name of the channel to search for.

    Returns:
    list: A list of dictionaries containing channel details (ID, title, description).
    """

    request = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id,snippet',
        maxResults=10
    )
    response = request.execute()

    channels_choice = []

    # Iterate over the first 5 items
    for item in response['items'][:10]:
        channel_id = item['snippet']['channelId']
        channel_title = item['snippet']['channelTitle']
        channel_description = item['snippet']['description']
        channels_choice.append({'channelId': channel_id, 'channelTitle': channel_title,
                                'channelDescription': channel_description})

    return channels_choice


if __name__ == "__main__":
    channels = youtube_channel_search("Totalbiscuit")
    for channel in channels:
        print(channel)
