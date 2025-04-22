from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, BooleanField
from wtforms.validators import DataRequired
from planner import generate_meal_plan
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class DietForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    goal = SelectField('Goal', choices=[('Weight Loss', 'Weight Loss'), ('Muscle Gain', 'Muscle Gain'), ('Maintenance', 'Maintenance')], validators=[DataRequired()])
    vegan = BooleanField('Vegan')
    diabetic = BooleanField('Diabetic')
    calories = IntegerField('Target Calories', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DietForm()

    if form.validate_on_submit():
        diet = []
        if form.vegan.data:
            diet.append("vegan")
        if form.diabetic.data:
            diet.append("diabetic")

        user_data = {
            "age": form.age.data,
            "gender": form.gender.data,
            "goal": form.goal.data,
            "diet": diet,
            "calories": form.calories.data
        }

        plan = generate_meal_plan(user_data)
        return render_template('meal_plan.html', plan=plan)

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
