from flask import Flask, render_template, request, redirect, abort
import random
import string
import sqlite3

app = Flask(__name__)
DB_NAME = "urls.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None

    if request.method == "POST":
        long_url = request.form.get("long_url")
        short_code = generate_short_code()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
            (short_code, long_url)
        )
        conn.commit()
        conn.close()

        short_url = request.host_url + short_code

    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT long_url, clicks FROM urls WHERE short_code = ?",
        (short_code,)
    )
    row = cur.fetchone()

    if row:
        long_url, clicks = row
        cur.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,)
        )
        conn.commit()
        conn.close()
        return redirect(long_url)
    else:
        conn.close()
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
