from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class PowerForm(FlaskForm):
	currlimit = SelectField('Select Charge Current Limit', choices=[('currtime 0 1', 'Stop Charging'),('currtime 6000 1', '6 000 mA (~3,9 kW 3-fas / ~1,2 kW 1-fas)'), ('currtime 8000 1', '8 000 mA (~5,2 kW 3-fas / ~1,6 kW 1-fas)'), ('currtime 10000 1', '10 000 mA (~6,5 kW 3-fas / ~2,1 kW 1-fas)'), ('currtime 12000 1', '12 000 mA (~8,1 kW 3-fas / ~2,7 kW 1-fas)'), ('currtime 14000 1', '14 000 mA (~9,3 kW 3-fas / ~3,0 kW 1-fas)'), ('currtime 16000 1', '16 000 mA (~10,1 kW 3-fas / ~3,4 kW 1-fas)'), ('currtime 18000 1', '18 000 mA (~10,1 kW 3-fas / ~3,9 kW 1-fas)'), ('currtime 20000 1', '20 000 mA (~10,1 kW 3-fas / ~4,4 kW 1-fas)')], validators=[DataRequired()])
	submit = SubmitField('Set Charge Current')
	# &#32; - html space

#class LoginForm(FlaskForm):
#	username = StringField('Username', validators=[DataRequired()])
#	password = PasswordField('Password', validators=[DataRequired()])
#	remember_me = BooleanField('Remember Me')
#	submit = SubmitField('Sign In')