from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class SampleForm(FlaskForm):
    sample_name = StringField("Sample Name", validators=[DataRequired(), Length(min=1, max=255)])
    description = StringField("Brief Description", validators=[DataRequired(), Length(min=1, max=255)])
    bpm = IntegerField("BPM (Beats Per Minute)", validators=[DataRequired(), Length(min=1, max=3)])
    key = StringField("Key (If Applicable)", validators=[Length(min=1, max=25)])
    file_path = FileField("Upload File Here")
    submit = SubmitField("submit")
