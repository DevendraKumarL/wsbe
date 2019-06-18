const mongoose = require("mongoose"),
    Schema = mongoose.Schema;

const modelName = "mailsettings";
let mailSettingsSchema = new Schema({
    from_: String,
    from_name: String,
    to_: String,
    to_name: String
});

mailSettingsSchema.statics.findAll = function(callback) {
    return this.find(callback);
};

let MailSettings = mongoose.model(modelName, mailSettingsSchema);

module.exports = MailSettings;
