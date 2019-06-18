const mongoose = require("mongoose"),
	Schema = mongoose.Schema;

const modelName = "report";
let reportSchema = new Schema({
	report_date: Date,
	ws_start: Date,
	ws_end: Date,
	project: String,
	bugzillaURL: String,
	highlights: String,
	codeReviews: String,
	planForWeek: String
});

reportSchema.statics.findAll = function(callback) {
	return this.find(callback);
};

let WSReport = mongoose.model(modelName, reportSchema);

module.exports = WSReport;
