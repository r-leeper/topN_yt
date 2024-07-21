from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from back_end.channel_search import youtube_channel_search

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def channel_search():
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

    # # For demonstration, we'll use a placeholder list of results
    # results = [
    #     {"title": "Example Channel 1", "description": "This is a description for Example Channel 1.", "id": "12345"},
    #     {"title": "Example Channel 2", "description": "This is a description for Example Channel 2.", "id": "23456"},
    #     {"title": "Example Channel 3", "description": "This is a description for Example Channel 3.", "id": "34567"},
    #     {"title": "Example Channel 4", "description": "This is a description for Example Channel 4.", "id": "45678"},
    #     {"title": "Example Channel 5", "description": "This is a description for Example Channel 5.", "id": "56789"},
    # ]
    return render_template('channel_results.html', query=query, results=results)


@app.route('/video_search', methods=['GET', 'POST'])
def video_search():
    if request.method == 'POST':
        title = request.args.get('title', 'Default Title')
        date_option = request.args.get('date_option', 'all-time')
        from_date = request.args.get('from_date', '')
        to_date = request.args.get('to_date', '')
        for_each = request.args.get('for_each', 'year')
        top = request.args.get('top', '1')
        sort_option = request.args.get('sort_option', 'newest')
        views_likes = request.args.get('views_likes', 'views')

        # Logic to filter videos based on search options
        # For testing, using static video list from file
        file_path = 'mock_data/youtube_videos.csv'
        videos_df = pd.read_csv(file_path, sep='~', usecols=['title', 'view_count'], nrows=50)
        results_html = videos_df.to_html(escape=False, index=False)

        return results_html

    return render_template('video_results.html', title=request.args.get('title', 'Default Title'))


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')
    if email:
        # Call your function to send the email with the dataframe
        send_email_with_results(email)
        return jsonify({'message': 'Email sent successfully!'})
    return jsonify({'error': 'Email is required.'}), 400


def send_email_with_results(email):
    # This function should handle sending the email with the dataframe
    # You need to implement this function yourself
    print(f"Sending email to {email} with the results...")


if __name__ == '__main__':
    app.run(debug=True)
