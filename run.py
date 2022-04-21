"""

"""

import json

from datetime import datetime
from slugify import slugify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    flash,
    request,
    url_for,
    redirect,
    render_template,
)
from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    current_user,
    LoginManager,
    login_required,
)

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["DEVELOPMENT"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "5791fcasxth5899863986498hggshdf"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:@MAwingu/..@db/postgres"

db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

all_reports = [
    {
        "name": "Refinary Plant Laboratory Report",
        "department": "Plants",
        "date_created": "2022-04-12",
        "report_uri": "/reports/1"
    },
    {
        "name": "Fractionation Plant Laboratory Report",
        "department": "Plants",
        "date_created": "2022-04-12",
        "report_uri": "/reports/2",
    },
]

refinary_lab_reports = []
refinary_additional_tests = [
    {
        "test_id": 0,
        "test": "FATTY ACID CONTENT %",
        "specs": "70%min",
        "time1": "",
        "analysis1": "",
        "time2": "",
        "analysis2": "",
        "time3": "",
        "analysis3": "",
    },
    {
        "test_id": 1,
        "test": "PEROXIDE VALUE (me) ",
        "specs": "Nil-RBD oil",
        "time1": "",
        "analysis1": "",
        "time2": "",
        "analysis2": "",
        "time3": "",
        "analysis3": "",
    },
    {
        "test_id": 2,
        "test": "INSOLUBLE IMPURITIES %",
        "specs": "0.07%max",
        "time1": "",
        "analysis1": "",
        "time2": "",
        "analysis2": "",
        "time3": "",
        "analysis3": "",
    },
    {
        "test_id": 3,
        "test": "SOAP CONTENT  %",
        "specs": "0.003% max",
        "time1": "",
        "analysis1": "",
        "time2": "",
        "analysis2": "",
        "time3": "",
        "analysis3": "",
    },
]

class User(db.Model, UserMixin):
    """

    """

    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, default=1)
    deleted = db.Column(db.Integer, nullable=False, default=0)
    suspended = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_id(self):
        return (self.user_id)


@app.before_first_request
def initialize_requirements():
    """

    """

    try:

        db.create_all()

    except Exception as error:
        print(error)

@login_manager.user_loader
def load_user(user_id):
    """

    """

    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    """

    """

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":

        error = ""

        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user:
            error = "Username already taken!"

        user = User.query.filter_by(email=email).first()

        if user:
            error = "Email already in use!"

        if error:
            flash(error, "danger")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(
                                    password).decode("utf-8")

        user = User(
                email=email, 
                username=username, 
                password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. You are now able to login", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    """

    """

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get("next")
            flash("Login Successful. Welcome Back!", "success")
            return redirect(next_page) if next_page else redirect(url_for("index"))

        flash("Login Unsuccessful. Please check email and password.", "danger")

    return render_template("login.html" , title="Login")

@app.route("/logout")
def logout():
    """

    """

    logout_user()
    return redirect(url_for("index"))

@app.route("/")
@app.route("/home", methods=["GET"])
@login_required
def index():
    """

    """

    return render_template(
        "home.html",
        all_reports=all_reports,
        title="All Reports",
    )

@app.route("/reports/1", methods=["GET", "POST"])
@login_required
def refinary_plant_lab():
    """
    
    """

    if request.method == "POST":

        form_data = dict(request.form)

        current_report = {}

        current_report["approved"] = ""
        current_report["approve_note"] = ""
        current_report["ffa"] = form_data["ffa"]
        current_report["time"] = form_data["time"]
        current_report["odour"] = form_data["odour"]
        current_report["red_70"] = form_data["red-70"]
        current_report["ffa_specs"] = form_data["ffa-specs"]
        current_report["red_specs"] = form_data["red-specs"]
        current_report["flow_rate"] = form_data["flow-rate"]
        current_report["yellow_specs"] = form_data["yellow-specs"]
        current_report["report_id"] = len(refinary_lab_reports) + 1
        current_report["final_oil_temp"] = form_data["final-oil-temp"]
        current_report["visible_imp_2"] = form_data["visible-imp-2"]
        current_report["bleach_temp"] = form_data["bleach-temp"]
        current_report["deod_temp"] = form_data["deod-temp"]
        current_report["comments"] = form_data["comments"]

        refinary_lab_reports.append(current_report)

        flash("Plant lab report added!", "warning")
        return redirect(url_for("refinary_plant_lab"))

    return render_template(
        "refinary_plant_lab.html",
        lab_reports=refinary_lab_reports,
        additional_tests=refinary_additional_tests,
        title="Refinary plant laboratory report",
    )

@app.route("/reports/1/edit/<int:report_id>", methods=["GET", "POST"])
@login_required
def edit_refinary_plant_lab(report_id: int):
    """
    
    """

    report = next((row for row in refinary_lab_reports if \
                    row["report_id"] == int(report_id)), None)

    if request.method == "POST":

        print(report)

        flash("message", "warning")
        return redirect(url_for("refinary_plant_lab"))

    return render_template(
        "edit_refinary_plant_lab.html",
        report=report,
        title="Refinary plant laboratory report",
    )

@app.route("/reports/1/approve/<int:report_id>", methods=["GET", "POST"])
@login_required
def approve_refinary_plant_lab(report_id: int):
    """
    
    """

    report = next((row for row in refinary_lab_reports if \
                    row["report_id"] == int(report_id)), None)

    if request.method == "POST":

        color = ""
        message = ""
        form_data = dict(request.form)

        if form_data["approve"] == "approved":
            color = "success"
            report["approved"] = "approved"
            message = "Plant lab report has been approved!"
        else:
            color = "danger"
            report["approved"] = "reject"
            report["approve_note"] = form_data["note"]
            message = "Plant lab report has been rejected!"

        flash(message, color)
        return redirect(url_for("refinary_plant_lab"))

    return render_template(
        "approve_refinary_plant_lab.html",
        report=report,
        title="Refinary plant laboratory report",
    )

@app.route("/reports/2", methods=["GET"])
@login_required
def fractionation_plant_lab():
    """
    
    """

    return render_template(
        "fractionation_plant_lab.html",
        lab_reports=[],
        additional_tests=[],
        title="Fractionation plant laboratory report",
    )

"""
Dynamic forms
"""

@app.route("/forms", methods=["GET", "POST"])
@login_required
def index_1():
    """

    """

    with open("assets/all_forms.json") as file:
        all_forms = json.load(file)

    if request.method == "POST":
        current_date = datetime.now()
        form_data = dict(request.form)

        new_form = {
            "form_id": len(all_forms) + 1,
            "form_title": form_data["form_title"],
            "form_description": form_data["form_description"],
            "date_created": current_date.strftime("%Y-%m-%d"),
            "sections": [],
        }

        all_forms.append(new_form)

        with open("assets/all_forms.json", "w") as file:
            json.dump(all_forms, file)

        flash("New form successfully created", "success")
        return redirect(url_for("index_1"))

    return render_template(
        "dynamic/home.html",
        all_forms=all_forms,
        title="All Forms",
    )

@app.route("/form/<int:form_id>/edit", methods=["GET", "POST"])
@login_required
def form_edit_1(form_id: int):
    """

    """

    with open("assets/all_forms.json") as file:
        all_forms = json.load(file)

    form = next((row for row in all_forms if \
                    row["form_id"] == int(form_id)), None)

    if request.method == "POST":

        message = ""
        current_date = datetime.now()
        form_data = dict(request.form)

        if "type" in form_data and form_data["type"] == "section":
            new_section = {
                    "section_id": len(form["sections"]) + 1,
                    "section_title": form_data["section_title"],
                    "date_created": current_date.strftime("%Y-%m-%d"),
                    "section_type": form_data["section_type"],
                    "section_description": form_data["section_description"],
                    "questions_per_row": int(form_data["questions_per_row"]),
                    "questions": [],
                    "answers": [],
                }

            form["sections"].append(new_section)
            message = "New section successfully created"
        else:
            current_section = next((section for section in form["sections"] if \
                    section["section_id"] == int(form_data["section_id"])), None)

            new_question = {
                        "question_title": form_data["question_title"],
                        "answer_type": form_data["answer_type"],
                        "question_slug": slugify(form_data["question_title"]),
                    }

            current_section["questions"].append(new_question)
            message = "New question successfully created"

        with open("assets/all_forms.json", "w") as file:
            json.dump(all_forms, file)

        flash(message, "success")
        return redirect(url_for("form_edit_1", form_id=form["form_id"]))

    return render_template(
        "dynamic/edit.html",
        form=form,
        title=form["form_title"],
    )

@app.route("/form/<int:form_id>/fill", methods=["GET", "POST"])
@login_required
def form_fill_1(form_id: int):
    """

    """

    with open("assets/all_forms.json") as file:
        all_forms = json.load(file)

    form = next((row for row in all_forms if \
                    row["form_id"] == int(form_id)), None)

    if request.method == "POST":
        form_data = dict(request.form)
        current_section = next((section for section in form["sections"] if \
                    section["section_id"] == int(form_data["section_id"])), None)
    
        form_data.pop("section_id")    
        
        current_section["answers"].append(form_data)

        with open("assets/all_forms.json", "w") as file:
            json.dump(all_forms, file)

        flash("Form successfully filled", "success")
        return redirect(url_for("form_fill_1", form_id=form["form_id"]))

    return render_template(
        "dynamic/fill.html",
        form=form,
        title=form["form_title"],
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
