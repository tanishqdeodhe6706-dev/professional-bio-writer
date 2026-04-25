import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from tools.search import get_references

load_dotenv()

app = Flask(__name__)

def generate_bio(name, role, skills):
    print("Fetching from Tavily...")

    refs = get_references(role + " " + skills)

    extra = ""
    if refs:
        extra = refs[0][:150]

    short_bio = f"{name} is a {role} with skills in {skills}. {extra}"

    long_bio = f"""{name} is an experienced {role} specializing in {skills}.
With strong commitment to excellence, {name} has worked on multiple projects.
{extra}
They aim to grow and contribute effectively."""

    return short_bio, long_bio


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        skills = request.form["skills"]

        short_bio, long_bio = generate_bio(name, role, skills)

        return render_template("index.html",
                               short_bio=short_bio,
                               long_bio=long_bio)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)