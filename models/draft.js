const mongoose = require("mongoose"),
	Schema = mongoose.Schema;

const modelName = "draft";
let draftSchema = new Schema({
	report_date: Date,
	ws_start: Date,
	ws_end: Date,
	project: String,
	bugzillaURL: String,
	highlights: String,
	codeReviews: String,
	planForWeek: String
});

draftSchema.statics.findAll = function (callback) {
	return this.find(callback);
};

let DraftReport = mongoose.model(modelName, draftSchema);

module.exports = DraftReport;
