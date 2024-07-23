import pandas as pd
from datetime import datetime


def topN_videos(df, date_option, from_date, to_date, for_each, top, order, views_likes):

    # Convert publish date to datetime if it's not already
    df['published_date'] = pd.to_datetime(df['published_date'], utc=True)

    # Get the current time & convert the current time to a Pandas datetime object
    current_time = pd.to_datetime(datetime.now()).tz_localize('UTC')

    # Set a datetime for the day before YouTube was born
    earliest_time = pd.to_datetime(datetime(2005, 4, 22)).tz_localize('UTC')

    if date_option == 'all-time':  # all-time option
        df_filtered = df

    elif date_option == 'specific-date':  # specific date option

        if from_date == "" and to_date != "":  # to_date given, no from_date
            end_date = pd.to_datetime(to_date).tz_localize('UTC')
            df_filtered = df[(df['published_date'] >= earliest_time) & (df['published_date'] <= end_date)]

        elif from_date != "" and to_date == "":  # from_date give, no to_date
            start_date = pd.to_datetime(from_date).tz_localize('UTC')
            df_filtered = df[(df['published_date'] >= start_date) & (df['published_date'] <= current_time)]

        elif from_date != "" and to_date != "":  # both dates given
            start_date = pd.to_datetime(from_date).tz_localize('UTC')
            end_date = pd.to_datetime(to_date).tz_localize('UTC')
            df_filtered = df[(df['published_date'] >= start_date) & (df['published_date'] <= end_date)]

    # Define the resampling rule and period label format based on the 'for_each' parameter
    if for_each == 'year':
        resample_rule = 'Y'
        period_format = '%Y'
    elif for_each == 'quarter':
        resample_rule = 'Q'
        period_format = 'Q%q %Y'
    elif for_each == 'month':
        resample_rule = 'M'
        period_format = '%B %Y'
    elif for_each == 'week':
        resample_rule = 'W'
        period_format = '%U %Y'
    else:
        raise ValueError("Invalid value for 'for_each'. Choose from 'year', 'quarter', 'month', or 'week'.")

    # Resample and aggregate the data
    df_resampled = df_filtered.set_index('published_date').groupby(pd.Grouper(freq=resample_rule))

    # Create a list to store the results
    results = []

    # Convert top argument string to int
    top = int(top)

    for period, group in df_resampled:
        top_videos = group.nlargest(top, views_likes)
        top_videos['period'] = period
        # Format the period to the desired label
        if for_each == 'quarter':
            period_label = f"Q{((period.month-1)//3)+1} {period.year}"
        elif for_each == 'week':
            period_label = period.strftime('%U %Y')
        else:
            period_label = period.strftime(period_format)
        top_videos['period_label'] = period_label
        top_videos['rank'] = top_videos[views_likes].rank(method='first', ascending=False).astype(int)
        results.append(top_videos)

    # Concatenate the results into a single DataFrame
    final_df = pd.concat(results).reset_index(drop=True)

    # Sort the final DataFrame based on the 'order' parameter
    if order == 'newest':
        final_df = final_df.sort_values(by=['period', 'rank'], ascending=[False, True])
    elif order == 'oldest':
        final_df = final_df.sort_values(by=['period', 'rank'], ascending=[True, True])
    else:
        raise ValueError("Invalid value for 'order'. Choose from 'newest' or 'oldest'.")

    # Use video_id to create link
    final_df['link'] = 'https://www.youtube.com/watch?v=' + final_df.pop('video_id')

    # Drop the 'period' column and rename 'period_label' to 'period'
    final_df = final_df.drop(columns=['period']).rename(columns={'period_label': 'period'})

    # Rename columns to the pretty, specific titles
    final_df = final_df.rename(columns={
        'title': 'Title',
        'view_count': 'Views',
        'like_count': 'Likes',
        'period': 'Period',
        'rank': 'Rank',
        'link': 'Link'
    })

    # Modify the 'Link' column to display "LINK" and be clickable
    final_df['Link'] = final_df['Link'].apply(lambda x: f'<a href="{x}" target="_blank">View video</a>')

    # Format the 'Views' and 'Likes' columns to include commas
    final_df['Views'] = final_df['Views'].apply(lambda x: f'{x:,}')
    final_df['Likes'] = final_df['Likes'].apply(lambda x: f'{x:,}')

    return final_df


if __name__ == '__main__':
    # Example usage using .csv to save on API calls.
    channel_videos_df = pd.read_csv('test_data/youtube_video_populated.csv', sep='~')
    output = topN_videos(channel_videos_df, "specific-date", "2015-01-01", "2020-12-31",
                         "year", "3", "newest", "view_count")
    print(output)
