import os
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app
from app.forms import PowerForm
from werkzeug.urls import url_parse
import sys, socket


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
		limit = form.currlimit.data
		limitb = limit.encode(encoding='utf-8')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(limitb, (ip, port))
		print("UDP sent to charger: " + limit)
		#tkmb.showinfo("UDP command", "UDP sent to charger: \n" + limit)
		flash('UDP sent to charger: '+ limit)
	return render_template('index.html', title='Home', form=form)