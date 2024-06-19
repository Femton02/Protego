const session = require("express-session")
const express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

// expected vulnerability
app.use(session({}))

// Ok
app.use(session({ name: "my-custom-session-name" }))