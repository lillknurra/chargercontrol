import os
import threading, time
from flask import render_template, flash, send_from_directory
from app import app
from app.forms import PowerForm, PermForm, SettingsForm
from werkzeug.urls import url_parse
import socket
from datetime import datetime

def thread_sock(wait, command, address):
	print('running thread ' + str(command))
	print('Sleep: ' + str(wait))
	print('IP: ' + address[0])
	print('Port: ' + str(address[1]))
	time.sleep(wait)
	print('wait time over!')
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(command, (address))
	print('UDP sent to charger: ' + str(command))

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = PowerForm()
	ip = app.config['HOST']
	port = int(app.config['PORT'])
	if form.validate_on_submit():
		now = datetime.now()
		current_hour = int(now.strftime('%H'))
		current_minute = int(now.strftime('%M'))
		start_hour = int(form.chrghour.data)
		start_minute = int(form.chrgminute.data)
		stop_hour = int(form.stophour.data)
		stop_minute = int(form.stopminute.data)
		show_display = True
		if start_hour == 100 or form.currlimit.data == 'currtime 0':
			wait_seconds = 1
			start_hour = current_hour
			start_minute = current_minute
			limit = form.currlimit.data + ' ' + str(wait_seconds)
			show_display = False
		elif start_hour >= current_hour:
			wait_seconds = (start_hour - current_hour) * 3600 + (start_minute - current_minute) * 60
			limit = form.currlimit.data + ' ' + str(wait_seconds)
		else:
			wait_seconds = (23 + start_hour - current_hour) * 3600 + (start_minute - current_minute) * 60
			limit = form.currlimit.data + ' ' + str(wait_seconds)
		if stop_hour != 100:
			if stop_hour >= start_hour:
				stop_wait = wait_seconds + (stop_hour - start_hour) * 3600 + (stop_minute - start_minute) * 60
			else:
				stop_wait = wait_seconds + (23 + stop_hour - start_hour) * 3600 + (stop_minute - start_minute) * 60
		if wait_seconds > 0:
			limitb = limit.encode(encoding='utf-8')
			#refreshb = ('currtime 0 1').encode(encoding='utf-8')
			#threadrefr = threading.Thread(target=thread_sock, args=(0.5, refreshb, (ip, port)))
			#threadrefr.start()
			threadlim = threading.Thread(target=thread_sock, args=(0.5, limitb, (ip, port)))
			threadlim.start()
			flash('UDP sent to charger: '+ limit)
			if show_display:
				if start_hour < 10:
					start_hour = '0' + str(start_hour)
				else:
					start_hour = str(start_hour)
				if start_minute == 0:
					start_minute = '00'
				else:
					start_minute = str(start_minute)
				display = 'display 0 0 0 0 ' + 'Charging$starts$' + start_hour + ':' + start_minute
				displayb = display.encode(encoding='utf-8')
				threaddisp = threading.Thread(target=thread_sock, args=(0.5, displayb, (ip, port)))
				threaddisp.start()
				flash('Charging set to start ' + start_hour + ':' + start_minute)
			else:
				flash('Charge command to take effect immediately!')
			if stop_hour != 100:
				if stop_wait > 0:
					stop = 'currtime 0 1'
					stopb = stop.encode(encoding='utf-8')
					threadstop = threading.Thread(target=thread_sock, args=(stop_wait, stopb, (ip, port)), daemon=True)
					threadstop.start()
					if stop_hour < 10:
						stop_hour = '0' + str(stop_hour)
					else:
						stop_hour = str(stop_hour)
					if stop_minute == 0:
						stop_minute = '00'
					else:
						stop_minute = str(stop_minute)
					flash('Charging set to stop ' + stop_hour + ':' + stop_minute)
				else:
					flash('Charge stop conditions faulty!!!')
		else:
			flash('Charge start conditions faulty!!!')
	return render_template('index.html', title='Home', form=form)

@app.route('/permanent', methods=['GET', 'POST'])
def permanent():
	form = PermForm()
	ip = app.config['HOST']
	port = int(app.config['PORT'])
	if form.validate_on_submit():
		limit = form.currlimit.data
		limitb = limit.encode(encoding='utf-8')
		threadlim = threading.Thread(target=thread_sock, args=(0.5, limitb, (ip, port)))
		threadlim.start()
		flash('UDP sent to charger: '+ limit)
		flash('Current limit command to take effect immediately!')
	return render_template('permanent.html', title='Permanent Limit', form=form)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
	form = SettingsForm()
	if form.validate_on_submit():
		ip = form.host.data
		app.config['HOST'] = ip
		print('Port set to: ' + ip)
		flash('Wallbox IP address updated to: ' + ip)
	return render_template('settings.html', title='Settings', form=form)

@app.route('/about')
def about():
	return render_template('about.html', title='About')