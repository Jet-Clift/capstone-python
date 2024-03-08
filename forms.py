from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, NumberRange

class SampleForm(FlaskForm):
    sample_name = StringField("Sample Name:", validators=[DataRequired(), Length(min=1, max=255)])
    description = StringField("Brief Description: ", validators=[DataRequired(), Length(min=1, max=255)])
    bpm = IntegerField("Beats Per Minute:", validators=[DataRequired(), NumberRange(min=1, max=300)])
    key = StringField("Key (Optional):", validators=[Length(min=1, max=25)])
    file_path = FileField("Upload File Here:")
    submit = SubmitField("Submit")
