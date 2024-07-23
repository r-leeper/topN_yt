import pandas as pd


def topN_videos(df, from_date, to_date, for_each, top, order, views_likes):
    # Convert publish date to datetime if it's not already
    df['published_date'] = pd.to_datetime(df['published_date'], utc=True)

    if from_date != "" or to_date != "":

        # Convert from_date and to_date to datetime objects
        start_date = pd.to_datetime(from_date).tz_localize('UTC')
        end_date = pd.to_datetime(to_date).tz_localize('UTC')

        # Filter the DataFrame by the specified date range
        df_filtered = df[(df['published_date'] >= start_date) & (df['published_date'] <= end_date)]

    else:
        df_filtered = df

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

    return final_df


if __name__ == '__main__':
    # Example usage using .csv to save on API calls.
    channel_videos_df = pd.read_csv('test_data/youtube_video_populated.csv', sep='~')
    output = topN_videos(channel_videos_df, "2015-01-01", "2020-01-01", "quarter", "3", "newest", "view_count")
    print(output)
