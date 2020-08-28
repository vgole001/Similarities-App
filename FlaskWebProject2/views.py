"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, abort, request, redirect
from FlaskWebProject2 import app
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
from helpers import lines, substrings
import re

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html')

@app.route("/compare", methods=["POST"])
def compare():
    """Handle requests for /compare via POST"""

    # Read files
    if not request.files["file1"] or not request.files["file2"]:
        abort(400, "missing file")
    try:
        file1 = request.files["file1"].read().decode("utf-8")
        file2 = request.files["file2"].read().decode("utf-8")
    except Exception:
        abort(400, "invalid file")

    # Compare files
    if not request.form.get("algorithm"):
        abort(400, "missing algorithm")
    elif request.form.get("algorithm") == "lines":
        regexes = [f"^{re.escape(match)}$" for match in lines(file1, file2)]
    elif request.form.get("algorithm") == "sentences":
        regexes = [re.escape(match) for match in sentences(file1, file2)]
    elif request.form.get("algorithm") == "substrings":
        if not request.form.get("length"):
            abort(400, "missing length")
        elif not int(request.form.get("length")) > 0:
            abort(400, "invalid length")
        regexes = [re.escape(match) for match in substrings(
            file1, file2, int(request.form.get("length")))]
    else:
        abort(400, "invalid algorithm")

    # Highlight files
    highlights1 = highlight(file1, regexes)
    highlights2 = highlight(file2, regexes)

    # Output comparison
    return render_template("compare.html", file1=highlights1, file2=highlights2)


def highlight(s, regexes):
    """Highlight all instances of regexes in s."""
    print('Regexes',regexes)
    # Get intervals for which strings match
    intervals = []
    for regex in regexes:
        if not regex:
            continue
        matches = re.finditer(regex, s, re.MULTILINE)
        for match in matches:
            intervals.append((match.start(), match.end()))
    intervals.sort(key=lambda x: x[0])
    print('Intervals:  ',intervals)
    # Combine intervals to get highlighted areas
    highlights = []
    for interval in intervals:
        if not highlights:
            highlights.append(interval)
            continue
        last = highlights[-1]

        # If intervals overlap, then merge them
        if interval[0] <= last[1]:
            new_interval = (last[0], interval[1])
            highlights[-1] = new_interval

        # Else, start a new highlight
        else:
            highlights.append(interval)

    print('Highlights: ',highlights)
    # Maintain list of regions: each is a start index, end index, highlight
    regions = []

    # If no highlights at all, then keep nothing highlighted
    if not highlights:
        regions = [(0, len(s), False)]

    # If first region is not highlighted, designate it as such
    elif highlights[0][0] != 0:
        regions = [(0, highlights[0][0], False)]

    # Loop through all highlights and add regions
    for start, end in highlights:
        if start != 0:
            prev_end = regions[-1][1]
            if start != prev_end:
                regions.append((prev_end, start, False))
        regions.append((start, end, True))

    # Add final unhighlighted region if necessary
    if regions[-1][1] != len(s):
        regions.append((regions[-1][1], len(s), False))

    # Combine regions into final result
    result = ""
    for start, end, highlighted in regions:
        escaped = escape(s[start:end])
        if highlighted:
            result += f"<span>{escaped}</span>"
        else:
            result += escaped
    return result

@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code
 

# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)







@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
