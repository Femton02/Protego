var serveIndex = require("serve-index")
var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

// expected vulnerability
app.use("/public", serveIndex(__dirname + "files"))

// Ok
app.use("/ftp", express.static("public/ftp"))

app.listen(3000)