import * as jose from 'jose'
var jwt = require("jsonwebtoken");

// expected vulnerability
var token = jwt.sign({ foo: "bar" }, "someSecret");


var token = jwt.sign({ foo: "bar" }, process.env.JWT_SECRET);
const jwt = await new jose.SignJWT({ 'urn:example:claim': true })
  .setIssuedAt()
  .setExpirationTime('2h')
  .sign(config.secret)

const jwt2 = await (new jose.SignJWT()).sign(config.secret)

console.log(jwt)