from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import re


app = Flask(__name__,
            template_folder='web_app/templates',
            static_folder='web_app/static')

app.config['SECRET_KEY'] = 'dev-key-314'

# Завантажуємо один файл і групуємо по record_type
df = pd.read_csv('web_app/static/all_codes.csv')
VALID_CODES = {
    record_type: set(group['code'].str.strip().str.upper())
    for record_type, group in df.groupby('record_type')
}


class CodeCheckForm(FlaskForm):
    codetype = RadioField(
        label='Тип коду',
        choices=[
            ('ICD10', 'Діагнози'),
            ('ACTION', 'Інтервенції'),
            ('LOINC', 'Спостереження'),
        ],
        validators=[DataRequired()]
    )
    checkcodes = TextAreaField(
        label='Коди для перевірки',
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Надіслати')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CodeCheckForm()
    result = None

    if form.validate_on_submit():
        raw = form.checkcodes.data
        codetype = form.codetype.data

        # Розбиваємо по комі, крапці з комою або новому рядку
        input_codes = {code.strip().upper() for code in re.split(r'[,;\n]+', raw) if code.strip()}

        # Вибираємо потрібний set по типу коду
        valid = VALID_CODES[codetype]

        if input_codes.issubset(valid):
            result = {'not_found': []}
        else:
            result = {'not_found': sorted(input_codes - valid)}

    return render_template('index.html', form=form, result=result)


if __name__ == "__main__":
    app.run(debug=True)
