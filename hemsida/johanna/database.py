from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()
    cur.close()
    
    return "Data inserted successfully!"

if __name__ == "__main__":
    app.run(debug=True)
