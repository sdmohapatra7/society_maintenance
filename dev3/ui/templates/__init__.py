from flask import Blueprint, render_template, session, redirect, url_for

template_bp = Blueprint("template", __name__)

@template_bp.route("/")
def home():
    return render_template("index.html")

@template_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("template.home"))
    return render_template("dashboard.html")
