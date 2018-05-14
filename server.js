const express = require("express"),
	bodyParser = require("body-parser"),
	mongoose = require("mongoose"),
	WSReport = require("./models/report"),
	DraftReport = require("./models/draft");

const app = express();

app.use(bodyParser.json());

const appPort = 5000;

let isConnectedToDB = false;
const dbURL = "mongodb://localhost:27017/wsdb"
mongoose.connect(dbURL);

let db = mongoose.connection;
db.on('error', (err) => {
	console.error.bind(err, "Mongodb connection error");
	isConnectedToDB = false;
});
db.on('open', () => {
	console.log("Mongodb connection successful");
	isConnectedToDB = true;
});

app.use((req, res, next) => {
	res.setHeader("Access-Control-Allow-Origin", "*");
	res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS");
	res.setHeader("Access-Control-Allow-Headers", "X-Requested-With,Content-Type");
	res.setHeader("Access-Control-Allow-Credentials", true);
	next();
});

app.post("/wsbe/report", (request, response) => {
	let data = {
		report_date: request.body.report_name,
		ws_start: request.body.ws_start,
		ws_end: request.body.ws_end,
		bugzillaURL: request.body.bugzillaURL,
		highlights: request.body.highlights,
		codeReviews: request.body.codeReviews,
		planForWeek: request.body.planForWeek
	};
	console.log("Report data: ", data);
	let report = new WSReport(data);

	report.save((err, report) => {
		if (err) {
			response.status(500).json({error: "Error saving the report"})
			return;
		}
		response.json({success: "Report recorded successfully"});
		return;
	});
});

app.get("/wsbe/reports", (request, response) => {
	WSReport.findAll((err, reports) => {
		if (err) {
			response.status(500).json({error: "Could not fetch reports"});
			return;
		}
		response.json(reports);
		return;
	});
});

app.post("/wsbe/draft", (request, response) => {
	DraftReport.findAll((err, report) => {
		console.log(request.body);
		if (err) {
			response.status(500).json({error: "Could not fetch draft report"});
			return;
		}
		if (report.length > 0 ){
			response.status(500).json({error: "A draft report already exists"});
			return;
		}
		let data = {
			report_date: request.body.report_date,
			ws_start: request.body.ws_start,
			ws_end: request.body.ws_end,
			bugzillaURL: request.body.bugzillaURL,
			highlights: request.body.highlights,
			codeReviews: request.body.codeReviews,
			planForWeek: request.body.planForWeek
		};
		console.log("Draft Report data: ", data);

		let draft = new DraftReport(data);
		draft.save((err, draft) => {
			if (err) {
				response.status(500).json({error: "Error saving the draft report"});
				return;
			}
			response.json({success: "Draft Report recorded successfully"});
			return;
		});
	});
});

app.put("/wsbe/draft", (request, response) => {
	DraftReport.findAll((err, draft) => {
		if (err) {
			response.status(500).json({error: "Could not fetch draft report"});
			return;
		}
		DraftReport.findByIdAndUpdate(draft[0]._id, request.body, {new: true}, (error, newDraft) => {
			if (error) {
				response.status(500).json({error: "Could not update draft report"});
				return;
			}
			response.json({updatedDraft: newDraft});
			return;
		});
	});
});

app.get("/wsbe/draft", (request, response) => {
	DraftReport.findAll((err, draft) => {
		if (err) {
			response.status(500).json({error: "Could not fetch draft report"});
			return;
		}
		response.json(draft);
		return;
	});
});

app.set("port", appPort);
app.listen(app.get("port"), '0.0.0.0', () => {
	console.log("wsbe-api app is running...");
});
