var jwt = require("jsonwebtoken");

// expected vulnerability
var token = jwt.sign({ foo: "bar" }, process.env.JWT_SECRET, {
	algorithm: "none",
});

var token2 = jwt.sign({ foo: "bar" }, process.env.JWT_SECRET, {
	algorithm: "ES256",
});