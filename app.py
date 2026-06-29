from xhtml2pdf import pisa
from flask import make_response
import os
from werkzeug.utils import secure_filename

from database import conn, cursor
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        if user:
            return redirect(url_for("home"))

        return "Invalid Email or Password"

    return render_template("login.html")


@app.route("/generate", methods=["POST"])
def generate():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    skills = request.form["skills"]
    skills_list = [skill.strip() for skill in skills.split(",")]
    education = request.form["education"]
    experience = request.form["experience"]
    summary = request.form["summary"]
    template = request.form["template"]
    photo = request.files["photo"]
    cursor.execute("""
    INSERT INTO users
    (name, email, password, phone, skills, education, experience)
     VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
    name,
    email,
    "",
    phone,
    skills,
    education,
    experience
    ))

    conn.commit()

    filename = ""

    if photo.filename != "":
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return render_template(
        "resume.html",
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        skills_list=skills_list,
        education=education,
        experience=experience,
        summary=summary,
        filename=filename,
        template=template
    
    )
@app.route("/download")
def download():

    html = render_template(
        "resume.html",
        name="Anjali Thakur",
        email="anjali@gmail.com",
        phone="9876543210",
        skills="Python, Flask, HTML",
        skills_list=["Python","Flask","HTML"],
        education="BCA",
        experience="Python Developer",
        summary="Python Developer",
        filename="",
        template="blue"
    )

    pdf = pisa.CreatePDF(html)

    response = make_response(pdf.dest.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=Resume.pdf"

    return response

if __name__ == "__main__":
    app.run(debug=True)
