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

def createEmail(to_name, from_name, report, project_name):
	highlights = report['highlights'].split("<br>")
	codeReviews = report['codeReviews'].split("<br>")
	planForWeek = report['planForWeek'].split("<br>")
	bugzillaURL = report['bugzillaURL'].split("<br>")
	ws_start = report['ws_start']
	ws_end = report['ws_end']
	project_name = project_name
	to_name = to_name
	from_name = from_name

	highlights_html  = ""
	codeReviews_html = ""
	planForWeek_html = ""
	for h in highlights:
		highlights_html  = highlights_html  + "<li>" + h + "</li>"
	for c in codeReviews:
		codeReviews_html = codeReviews_html + "<li>" + c + "</li>"
	for p in planForWeek:
		planForWeek_html = planForWeek_html + "<li>" + p + "</li>"

	return """
			Hi """ + to_name + """,<br>
			------------<br>
			<span>WSR for the Period: """ + ws_start + """ - """ + ws_end + """</span><br>
			<span>Project: """ + project_name + """</span>
			<ul>
				<li>
					Highlights
					<ul>""" + highlights_html + """</ul>
				</li>
				<li>
					Bugs
					<ul><li><a href='""" + bugzillaURL + """'>Bugzilla manager report for the above peroid</a></li></ul>
				</li>
				<li>
					Code Reviews
					<ul>""" + codeReviews_html + """</ul>
				</li>
				<li>
					Plan for this week
					<ul>""" + planForWeek_html + """</ul>
				</li>
			</ul>
			------------<br>
			Thanks,<br>
			""" + from_name + """<br><br>

			<i>*** Auto-generated using <a href="https://github.com/DevendraKumarL/wsreporter">WSReporter</a> ***</i>
			"""


@app.route('/wsmailer/sendmail-smtp', methods = ['POST'])
def sendmail_smtp():
	requestData = request.get_json()

	from_ = requestData['from_']
	from_name = requestData['from_name']
	to_ = requestData['to_']
	to_name = requestData['to_name']
	pass_ = requestData['pass_']
	report = requestData['report']

	subject_ = "WSR - " + report['report_date']
	body_ = createEmail(to_name, from_name, report, requestData['project_name'])

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
	report = requestData['report']

	subject_ = "WSR - " + report['report_date']
	body_ = createEmail(to_name, from_name, report, requestData['project_name'])

	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = to_
	mail.subject = subject_
	mail.HTMLBody = body_

	mail.Send()
	return jsonify({"success": "Email sent successfully"})


if (__name__):
	app.run()
