from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("event.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            event TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    event = request.form["event"]

    conn = sqlite3.connect("event.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO registrations (name,email,phone,event) VALUES (?,?,?,?)",
                (name,email,phone,event))
    conn.commit()
    conn.close()

    return redirect("/view")

@app.route("/view")
def view():
    conn = sqlite3.connect("event.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrations")
    data = cur.fetchall()
    conn.close()
    return render_template("view.html", data=data)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("event.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM registrations WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/view")

if __name__ == "__main__":
    app.run(debug=True)