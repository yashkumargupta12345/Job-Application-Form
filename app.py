from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_USERNAME"] = "flaskmail2233@gmail.com"
app.config["MAIL_PASSWORD"] = "apmv amvy gaur jcei"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
db = SQLAlchemy(app)

mail = Mail()


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last,
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = (f"New Form Submission.\n Hey! {first_name} here are your "\
                        f"credentials.\n Name: {first_name} {last}\n "
                        f"Availability: {date}\n Occupation: {occupation}\n"
                        f"Thank You!")

        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        mail.send(message)

        flash(f"Hey {first_name}! Your form has been submitted successfully")
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        mail.init_app(app)
        app.run(debug=True, port=5001)


