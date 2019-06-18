import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import win32com.client as win32

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def createEmail(to_name, from_name, report):
	to_name = to_name
	from_name = from_name

	return """
			Hi """ + to_name + """,<br>------------<br>""" + report + """
			------------<br>
			Thanks,<br>""" + from_name + """<br><br>
			<i>Auto-generated using <a href="https://github.com/DevendraKumarL/wsreporter">WSReporter</a></i>
			"""


@app.route('/wsmailer/sendmail-smtp', methods = ['POST'])
def sendmail_smtp():
	requestData = request.get_json()

	from_ = requestData['from_']
	from_name = requestData['from_name']
	to_ = requestData['to_']
	to_name = requestData['to_name']
	pass_ = requestData['pass_']
	report = requestData['reportHTML']

	r = requestData['report']
	subject_ = "WSR - " + r['report_date']
	body_ = createEmail(to_name, from_name, report)

	msg = MIMEMultipart()
	msg["From"] = from_
	msg["To"] = to_
	msg["Subject"] = subject_
	msg.attach(MIMEText(body_, "html"))

	emailContent = msg.as_string()

	server = smtplib.SMTP('smtp-mail.outlook.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	# TODO: handle authentication failure
	print "Logging into the server..."
	server.login(from_, pass_)

	print "Sending email..."
	server.sendmail(from_, to_, emailContent)
	print "Email sent..."

	server.quit()
	return jsonify({"success": "Email sent successfully"})

@app.route('/wsmailer/sendmail-outlook', methods = ['POST'])
def sendmail_outlook():
	requestData = request.get_json()

	from_name = requestData['from_name']
	to_ = requestData['to_']
	to_name = requestData['to_name']
	report = requestData['reportHTML']

	r = requestData['report']
	subject_ = "WSR - " + r['report_date']
	body_ = createEmail(to_name, from_name, report)

	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = to_
	mail.subject = subject_
	mail.HTMLBody = body_

	mail.Send()
	return jsonify({"success": "Email sent successfully"})


if (__name__):
	app.run()
