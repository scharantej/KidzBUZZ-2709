
# Import the necessary modules.
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Create a Flask application.
app = Flask(__name__)

# Configuring database
conn = sqlite3.connect('news.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id INTEGER PRIMARY KEY, title TEXT, author TEXT, date TEXT, content TEXT)''')
conn.commit()

# Define the home page route.
@app.route('/')
def home():
    # Get all articles from the database.
    c.execute('SELECT * FROM articles ORDER BY date DESC')
    articles = c.fetchall()
    # Render the home page, passing the articles to the template.
    return render_template('main.html', articles=articles)

# Define the article page route.
@app.route('/article/<int:article_id>')
def article(article_id):
    # Get the article with the given ID from the database.
    c.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
    article = c.fetchone()
    # Render the article page, passing the article to the template.
    return render_template('article.html', article=article)

# Define the search route.
@app.route('/search')
def search():
    # Get the search query from the request.
    query = request.args.get('q')
    # Get all articles from the database that contain the search query.
    c.execute('SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?', ('%' + query + '%', '%' + query + '%'))
    articles = c.fetchall()
    # Render the search results page, passing the articles to the template.
    return render_template('main.html', articles=articles)

# Define the trending route.
@app.route('/trending')
def trending():
    # Get all articles from the database, ordered by the number of views.
    c.execute('SELECT * FROM articles ORDER BY views DESC')
    articles = c.fetchall()
    # Render the trending page, passing the articles to the template.
    return render_template('main.html', articles=articles)

# Run the application.
if __name__ == '__main__':
    app.run(debug=True)
