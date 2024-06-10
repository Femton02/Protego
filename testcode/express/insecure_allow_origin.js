var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

app.get("/insecure", (req, res) => {
  var origin1 = req.params.origin
// expected vulnerability
  res.writeHead(200, { "Access-Control-Allow-Origin": req.params.origin })
// expected vulnerability
  res.set("access-control-allow-origin", origin1)
})


app.get("/insecure", (req, res) => {
    var origin2 = req.query.origin
  // expected vulnerability
    res.setHeader("Access-Control-Allow-Origin", origin2)
  })

// OK
app.get("/secure", (req, res) => {
    var origin3 = "https://some-origin"
    res.writeHead(200, { "Access-Control-Allow-Origin": "https://mish.bear" })
    res.set("access-control-allow-origin", origin3)
  })