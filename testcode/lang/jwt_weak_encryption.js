var jwt = require("jsonwebtoken");

// bearer:expected javascript_lang_jwt_weak_encryption
var token = jwt.sign({ foo: "bar" }, process.env.JWT_SECRET, {
	algorithm: "none",
});

var token2 = jwt.sign({ foo: "bar" }, process.env.JWT_SECRET, {
	algorithm: "ES256",
});