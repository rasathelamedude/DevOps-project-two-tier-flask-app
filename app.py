import os
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "devops_project")

mysql = MySQL(app)


def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS messages (
                  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  message VARCHAR(255)
                )
                """
        )
        mysql.connection.commit()
        cur.close()


@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT message FROM messages")
    messages = cur.fetchall()
    cur.close()
    return render_template("index.html", messages=messages)


@app.route("/submit", methods=["POST"])
def submit():
    new_message = request.form.get("new_message")
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (message) VALUES (%s)", [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": new_message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
