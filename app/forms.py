from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import app

class PowerForm(FlaskForm):
	currlimit = SelectField('Select Charger Current Limit', choices=[('currtime 0', 'Stop Charging Now'),('currtime 6000', '6 000 mA (~3,9 kW 3-fas / ~1,2 kW 1-fas)'), ('currtime 8000', '8 000 mA (~5,2 kW 3-fas / ~1,6 kW 1-fas)'), ('currtime 10000', '10 000 mA (~6,5 kW 3-fas / ~2,1 kW 1-fas)'), ('currtime 12000', '12 000 mA (~8,1 kW 3-fas / ~2,7 kW 1-fas)'), ('currtime 14000', '14 000 mA (~9,3 kW 3-fas / ~3,0 kW 1-fas)'), ('currtime 16000', '16 000 mA (~10,1 kW 3-fas / ~3,4 kW 1-fas)'), ('currtime 18000', '18 000 mA (~10,1 kW 3-fas / ~3,9 kW 1-fas)'), ('currtime 20000', '20 000 mA (~10,1 kW 3-fas / ~4,4 kW 1-fas)')], validators=[DataRequired()])
	chrghour = SelectField('Start: Hour', choices=[('100', 'Right away'), ('00', '00'),('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')], validators=None)
	chrgminute = SelectField('Start: Minute', choices=[('00', '00'), ('10', '10'),('20', '20'), ('30', '30'), ('40', '40'), ('50', '50')], validators=None)
	stophour = SelectField('Stop: Hour', choices=[('100', 'None'), ('00', '00'),('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')], validators=None)
	stopminute = SelectField('Stop: Minute', choices=[('00', '00'), ('10', '10'),('20', '20'), ('30', '30'), ('40', '40'), ('50', '50')], validators=None)
	submit = SubmitField('Setup Charging')

	# &#32; - html space

class PermForm(FlaskForm):
	currlimit = SelectField('Select Charger Current Limit', choices=[('curr 6000', '6 000 mA (~3,9 kW 3-fas / ~1,2 kW 1-fas)'), ('curr 8000', '8 000 mA (~5,2 kW 3-fas / ~1,6 kW 1-fas)'), ('curr 10000', '10 000 mA (~6,5 kW 3-fas / ~2,1 kW 1-fas)'), ('curr 12000', '12 000 mA (~8,1 kW 3-fas / ~2,7 kW 1-fas)'), ('curr 14000', '14 000 mA (~9,3 kW 3-fas / ~3,0 kW 1-fas)'), ('curr 16000', '16 000 mA (~10,1 kW 3-fas / ~3,4 kW 1-fas)'), ('curr 18000', '18 000 mA (~10,1 kW 3-fas / ~3,9 kW 1-fas)'), ('curr 20000', '20 000 mA (~10,1 kW 3-fas / ~4,4 kW 1-fas)')], validators=[DataRequired()])
	submit = SubmitField('Set Current Limit')

class SettingsForm(FlaskForm):
	ip = app.config['HOST']
	host = StringField('Enter Wallbox IP address', default=ip, validators=[DataRequired()])
	submit = SubmitField('Set IP adress')

#class LoginForm(FlaskForm):
#	username = StringField('Username', validators=[DataRequired()])
#	password = PasswordField('Password', validators=[DataRequired()])
#	remember_me = BooleanField('Remember Me')
#	submit = SubmitField('Sign In')