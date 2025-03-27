from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_articles():
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT title, link, date FROM headlines WHERE date >= '2022-01-01' ORDER BY date DESC")
    articles = c.fetchall()
    conn.close()
    return articles

@app.route("/")
def home():
    articles = get_articles()
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run()
