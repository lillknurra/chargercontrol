import os
from time import sleep
#from turtle import delay
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app
from app.forms import PowerForm
from werkzeug.urls import url_parse
import sys, socket
from datetime import datetime


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = PowerForm()
	ip = "192.168.99.143"
	port = 7090
	if form.validate_on_submit():
		now = datetime.now()
		current_hour = int(now.strftime('%H'))
		current_minute = int(now.strftime('%M'))
		current_second = int(now.strftime('%S'))
		start_hour = int(form.chrghour.data)
		start_minute = int(form.chrgminute.data)
		show_display = True
		if start_hour == 100 or form.currlimit.data == 'currtime 0':
			limit = form.currlimit.data + ' 1'
			show_display = False
		elif start_hour > current_hour:
			wait_seconds = (start_hour - current_hour) * 3600 + (start_minute - current_minute) * 60
			limit = form.currlimit.data + ' ' + str(wait_seconds)
		else:
			wait_seconds = (23 + start_hour - current_hour) * 3600 + (start_minute - current_minute) * 60
			limit = form.currlimit.data + ' ' + str(wait_seconds)
		limitb = limit.encode(encoding='utf-8')
		refreshb = ('currtime 0 1').encode(encoding='utf-8')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(refreshb, (ip, port))
		sleep(1)
		sock.sendto(limitb, (ip, port))
		sleep(1)
		if show_display:
			start_hour = str(start_hour)
			if start_minute == 0:
				start_minute = '00'
			else:
				start_minute = str(start_minute)
			display = 'display 0 0 0 0 ' + 'Charging$starts$' + start_hour + ':' + start_minute
			displayb = display.encode(encoding='utf-8')
			sock.sendto(displayb, (ip, port))
		print('UDP sent to charger: ' + limit + '\nCharging set to start ' + start_hour + ':' + start_minute)
		#tkmb.showinfo("UDP command", "UDP sent to charger: \n" + limit)
		flash('UDP sent to charger: '+ limit)
		flash('Charging set to start ' + start_hour + ':' + start_minute)
	return render_template('index.html', title='Home', form=form)