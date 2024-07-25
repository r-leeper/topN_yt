from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pandas as pd
from back_end.channel_search import youtube_channel_search
from back_end.youtube_video_populate import youtube_video_populate
from back_end.video_search import topN_videos
from back_end.email_user_df import send_df_as_email
from flask_session import Session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.urandom(24)
Session(app)


@app.route('/', methods=['GET', 'POST'])
def channel_search():
    # Path to the flask_session directory
    if request.method == 'POST':

        channel_search_query = request.form['search']
        # Redirect to the results page with the query as a parameter
        return redirect(url_for('channel_results', query=channel_search_query))
    return render_template('channel_search.html')


@app.route('/channel_results')
def channel_results():
    # Get query
    query = request.args.get('query')

    # Get results
    results = youtube_channel_search(query)

    session.pop('videos_df', None)

    return render_template('channel_results.html', query=query, results=results)


@app.route('/video_search', methods=['GET', 'POST'])
def video_search():

    if 'channel_title' not in session:
        session['channel_title'] = request.args.get('channelTitle')

    if request.method == 'POST':
        channel_id = request.form.get('channel_id')
        date_option = request.form.get('date_option', 'all-time')
        from_date = request.form.get('from_date', '')
        to_date = request.form.get('to_date', '')
        for_each = request.form.get('for_each', 'year')
        top = request.form.get('top', '1')
        sort_option = request.form.get('sort_option', 'newest')
        views_likes = request.form.get('views_likes', 'views')

        # Check if dataframe is already in session
        if 'all_videos_df' not in session:
            # Get the dataframe using youtube_video_populate function
            all_videos_df = youtube_video_populate(channel_id)
            # Convert dataframe to JSON and store in session
            session['all_videos_df'] = all_videos_df.to_json()

        # Logic to filter videos based on search options
        all_videos_df = pd.read_json(session['all_videos_df'])

        topN_df = topN_videos(all_videos_df, date_option, from_date, to_date, for_each, top, sort_option, views_likes)

        session['topN_df'] = topN_df.to_json()
        print("Session key set:", 'topN_df' in session)

        results_html = topN_df.to_html(escape=False, index=False)

        return results_html

    return render_template('video_results.html', title=request.args.get('channelTitle'),
                           channelId=request.args.get('channelId'))


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')
    if email:
        print("Session key set from email:", 'topN_df' in session)
        topN_df = pd.read_json(session['topN_df'])
        channel_title = session.get('channel_title', 'Not set')
        print(f"This is coming from the send_email function {channel_title}")
        # Call your function to send the email with the dataframe
        send_df_as_email(df_to_send=topN_df, recipient_email=email, channel_name=channel_title)
        return jsonify({'message': 'Email sent successfully!'})
    return jsonify({'error': 'Email is required.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
