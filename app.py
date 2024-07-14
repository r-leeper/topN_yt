from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def channel_search():
    if request.method == 'POST':
        search_query = request.form['search']
        # Process the search query here
        # For now, redirect to the results page with the query as a parameter
        return redirect(url_for('search_results', query=search_query))
    return render_template('channel_search.html')


@app.route('/results')
def search_results():
    query = request.args.get('query')
    # Perform the search and get results
    # For demonstration, we'll use a placeholder list of results
    results = [
        {"title": "Example Channel 1", "description": "This is a description for Example Channel 1.", "id": "12345"},
        {"title": "Example Channel 2", "description": "This is a description for Example Channel 2.", "id": "23456"},
        {"title": "Example Channel 3", "description": "This is a description for Example Channel 3.", "id": "34567"},
        {"title": "Example Channel 4", "description": "This is a description for Example Channel 4.", "id": "45678"},
        {"title": "Example Channel 5", "description": "This is a description for Example Channel 5.", "id": "56789"},
    ]
    return render_template('channel_results.html', query=query, results=results)


@app.route('/video_search', methods=['GET'])
def video_search():
    title = request.args.get('title', 'Default Title')
    date_option = request.args.get('date_option', 'all-time')
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    for_each = request.args.get('for_each', 'year')
    top = request.args.get('top', '1')
    sort_option = request.args.get('sort_option', 'newest')

    # Logic to filter videos based on search options
    # For demonstration, using static video list
    videos = [{'title': 'Sample Video 1', 'description': 'Description 1'},
              {'title': 'Sample Video 2', 'description': 'Description 2'}]

    return render_template('video_results.html', title=title, videos=videos)


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


if __name__ == '__main__':
    app.run(debug=True)
