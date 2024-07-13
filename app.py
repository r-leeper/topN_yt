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
        {"title": "Example Channel 1", "description": "This is a description for Example Channel 1."},
        {"title": "Example Channel 2", "description": "This is a description for Example Channel 2."}
    ]
    return render_template('channel_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
