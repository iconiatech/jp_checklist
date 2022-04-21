"""

"""

from datetime import datetime
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

all_sections = []
all_forms = [
    {
        "form_id": 1, 
        "form_title": "Guest details at the gate",
        "form_tabbed": False,
        "created_by": "petergich", "next_due": "2021-12-12 20:00",
        "created_on": "2021-12-12",
    },
]
all_lab_reports = [
    {
        "time": "", "ffa_specs": "", "red_specs": "",
        "yellow_specs": "", "odour": "", "visible_imp_1": "",
        "flow_rate": "", "final_oil_temp": "", "ffa": "",
        "red_70": "", "visible_imp_2": "", "bleach_temp": "",
        "deod_temp": "", "comments": "", "report_id": 0,
    },
    {
        "time": "", "ffa_specs": "", "red_specs": "",
        "yellow_specs": "", "odour": "", "visible_imp_1": "",
        "flow_rate": "", "final_oil_temp": "", "ffa": "",
        "red_70": "", "visible_imp_2": "", "bleach_temp": "",
        "deod_temp": "", "comments": "", "report_id": 1,
    },
    {
        "time": "", "ffa_specs": "", "red_specs": "",
        "yellow_specs": "", "odour": "", "visible_imp_1": "",
        "flow_rate": "", "final_oil_temp": "", "ffa": "",
        "red_70": "", "visible_imp_2": "", "bleach_temp": "",
        "deod_temp": "", "comments": "", "report_id": 2,
    },
    {
        "time": "", "ffa_specs": "", "red_specs": "",
        "yellow_specs": "", "odour": "", "visible_imp_1": "",
        "flow_rate": "", "final_oil_temp": "", "ffa": "",
        "red_70": "", "visible_imp_2": "", "bleach_temp": "",
        "deod_temp": "", "comments": "", "report_id": 3,
    },
    {
        "time": "", "ffa_specs": "", "red_specs": "",
        "yellow_specs": "", "odour": "", "visible_imp_1": "",
        "flow_rate": "", "final_oil_temp": "", "ffa": "",
        "red_70": "", "visible_imp_2": "", "bleach_temp": "",
        "deod_temp": "", "comments": "", "report_id": 4,
    },
]
additional_tests = [
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

    additional_tests.sort(key=lambda x: x.get("test_id"), reverse=False)
    all_lab_reports.sort(key=lambda x: x.get("report_id"), reverse=False)

    return render_template(
        "home.html",
        lab_reports=all_lab_reports,
        additional_tests=additional_tests,
        title="REFINERY PLANT LABORATORY REPORT",
    )

@app.route("/lab_reports", methods=["POST", "GET"])
@login_required
def lab_reports():
    """

    """

    if request.method == "POST":

        error = ""
        current_date = datetime.now()
        form_data = dict(request.form)

        if "additional" in form_data:
            if "test-id" not in form_data:
                error = "Please select the test to be added."

            if error:
                flash(error, "danger")
                return redirect(url_for("index"))

            additional_tests.sort(key=lambda x: x.get("test_id"), reverse=False)

            current_test = additional_tests[int(form_data["test-id"])]

            current_test["time1"] = form_data["time1"]
            current_test["time2"] = form_data["time2"]
            current_test["time3"] = form_data["time3"]

            current_test["analysis1"] = form_data["analysis1"]
            current_test["analysis2"] = form_data["analysis2"]
            current_test["analysis3"] = form_data["analysis3"]

        else:
            lab_report = dict(
                            report_id=len(all_lab_reports) + 1,
                            time=form_data["time"],
                            ffa_specs=form_data["ffa-specs"],
                            red_specs=form_data["red-specs"],
                            yellow_specs=form_data["yellow-specs"],
                            odour=form_data["odour"],
                            visible_imp_1=form_data["visible-imp-1"],
                            flow_rate=form_data["flow-rate"],
                            final_oil_temp=form_data["final-oil-temp"],
                            ffa=form_data["ffa"],
                            red_70=form_data["red-70"],
                            visible_imp_2=form_data["visible-imp-2"],
                            bleach_temp=form_data["bleach-temp"],
                            deod_temp=form_data["deod-temp"],
                            comments=form_data["comments"],
                            date_created=current_date,
                        )

            all_lab_reports.append(lab_report)

    flash("New lab report added!", "success")
    return redirect(url_for("index"))

@app.route("/update_reports", methods=["POST"])
@login_required
def update_reports():

    if request.method == "POST":

        form_data = dict(request.form)

        all_lab_reports.sort(key=lambda x: x.get("report_id"), reverse=False)
        current_report = all_lab_reports[int(form_data["report-id"])]

        current_report["time"] = form_data["time"]
        current_report["ffa_specs"] = form_data["ffa-specs"]
        current_report["red_specs"] = form_data["red-specs"]
        current_report["yellow_specs"] = form_data["yellow-specs"]
        current_report["odour"] = form_data["odour"]
        current_report["flow_rate"] = form_data["flow-rate"]
        current_report["final_oil_temp"] = form_data["final-oil-temp"]
        current_report["ffa"] = form_data["ffa"]
        current_report["red_70"] = form_data["red-70"]
        current_report["visible_imp_2"] = form_data["visible-imp-2"]
        current_report["bleach_temp"] = form_data["bleach-temp"]
        current_report["deod_temp"] = form_data["deod-temp"]
        current_report["comments"] = form_data["comments"]

    flash("Plant lab report updated!", "warning")
    return redirect(url_for("index"))

@app.route("/forms", methods=["GET"])
@login_required
def forms():
    """

    """

    return render_template(
        "forms.html",
        title="Forms",
        forms=all_forms,
    )

@app.route("/form/create", methods=["POST"])
@login_required
def form_create():
    """

    """

    if request.method == "POST":
        current_date = datetime.now()
        form_data = dict(request.form)
        form_tabbed = True if "tabbed-section" in form_data else False

        new_form = dict(
                        created_by="petergich",
                        form_tabbed=form_tabbed,
                        form_id=len(all_forms) + 1,
                        next_due=False,
                        form_title=form_data["form-title"],
                        form_description=form_data["description"],
                        created_on=current_date.strftime("%Y-%m-%d"),
                    )

        all_forms.append(new_form)

    flash("Form successfully added!", "success")
    return redirect(url_for("forms"))

@app.route("/form/<int:form_id>/edit", methods=["GET", "POST"])
@login_required
def form_edit(form_id: int):
    """

    """

    if request.method == "POST":

        form_data = dict(request.form)

        if "type" in form_data and form_data["type"] == "section":

            new_section = dict(
                            form_id=form_id,
                            defaults_keys=[],
                            section_id=len(all_sections) +1,
                            section_type=form_data["section_type"],
                            section_title=form_data["section_title"],
                            section_description=form_data["section_description"],
                            questions=[],
                        )
            all_sections.append(new_section)

        elif "type" in form_data and form_data["type"] == "question":
            current_section = next((section for section in all_sections if \
                    section["section_id"] == int(form_data["section_id"])), None)

            new_question = dict(
                                question_title=form_data["question_title"],
                                answer_type=form_data["answer_type"],
                            )

            current_section["questions"].append(new_question)

    all_forms.sort(key=lambda x: x.get("form_id"))
    form = next((form for form in all_forms if \
                    form["form_id"] == int(form_id)), None)

    test_sections = [
        {
            "form_id": form_id,
            "section_id": 1,
            "section_type": "type_a",
            "section_title": "Section A",
            "section_description": "Little description here",
            "questions": [
                {
                    "question_title": "First Name",
                    "answer_type": "text",
                },
                {
                    "question_title": "Last Name",
                    "answer_type": "text",
                },
                {
                    "question_title": "Age",
                    "answer_type": "number",
                },
            ],
        },
        {
            "form_id": form_id,
            "section_id": 2,
            "section_type": "type_b",
            "section_title": "Section B",
            "section_description": "Guear details",
            "defaults_keys": [
                {
                    "key_name": "Guard Name",
                    "values": ["Peter Gichia", "Kevin Hart"],
                },
                {
                    "key_name": "Position",
                    "values": ["Manager", "Sub"],
                },
            ],
            "questions": [
                {
                    "question_title": "Gate No",
                    "answer_type": "text",
                },
                {
                    "question_title": "Supervisor",
                    "answer_type": "text",
                },
                {
                    "question_title": "Time of day",
                    "answer_type": "number",
                },
            ],
        },
    ]

    # sections = [section for section in test_sections if section["form_id"] == form_id]
    sections = [section for section in all_sections if section["form_id"] == form_id]

    return render_template(
        "form_edit.html",
        form=form,
        sections=sections,
        questions=[],
        title=form["form_title"],
    )

@app.route("/section/<int:form_id>/defaults", methods=["POST"])
@login_required
def add_defaults(form_id: int):
    """

    """

    if request.method == "POST":

        message = ""
        form_data = dict(request.form)

        current_section = next((section for section in all_sections if \
                section["section_id"] == int(form_data["section_id"])), None)

        if "type" in form_data and form_data["type"] == "key":

            new_default = dict(key_name=form_data["default_title"], values=[])
            current_section["defaults_keys"].append(new_default)

            message = "New default key added."

        else:

            i = 0
            for key in current_section["defaults_keys"]:
                if key["key_name"] == form_data["key_name"]:
                    current_section["defaults_keys"][i]["values"].append(form_data["default_value"])
                i += 1

            message = "New default value added."

    flash(message, "success")
    return redirect(url_for("form_edit", form_id=form_id))

@app.route("/form/<int:form_id>/fill", methods=["GET", "POST"])
@login_required
def form_fill(form_id: int):
    """

    """

    all_forms.sort(key=lambda x: x.get("form_id"))

    form = next((form for form in all_forms if \
                    form["form_id"] == int(form_id)), None)

    sections = [section for section in all_sections if section["form_id"] == form_id]

    return render_template(
        "form_fill.html",
        form=form,
        sections=sections,
        title=form["form_title"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
