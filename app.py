"""Import libraries."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Food(db.Model):
    """Food database class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        """Return food name."""
        return f"Food('{self.name}')"


class FoodForm(FlaskForm):
    """Food Form."""

    name = StringField("Food", validators=[DataRequired()])
    submit = SubmitField("Add")


@app.route("/", methods=["GET", "POST"])
def home():
    """Return homepage."""
    form = FoodForm()
    if form.validate_on_submit():
        name = form.name.data
        food = Food(name=name)
        db.session.add(food)
        db.session.commit()
        form.name.data = ""
    return render_template("index.html", form=form)


@app.route("/food", methods=["GET"])
def get_food():
    """Look inside database."""
    print(f"\n{Food.query.all()}\n")
    return ""


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
