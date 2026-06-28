from xhtml2pdf import pisa
from flask import make_response
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    skills = request.form["skills"]
    skills_list = [skill.strip() for skill in skills.split(",")]
    education = request.form["education"]
    experience = request.form["experience"]
    template = request.form["template"]
    photo = request.files["photo"]

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
