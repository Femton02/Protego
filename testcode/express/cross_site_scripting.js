const express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

app.get("/bad", (req, res) => {
// expected vulnerability
  res.send("<p>" + req.body.customer.name + "</p>")
})

app.get("/bad-2", (req, res) => {
// expected vulnerability
  res.send("<p>" + req.body["user_id"] + "</p>")
})

app.get("/bad", (req, res) => {
    var customerName = req.body.customer.name
  // expected vulnerability
  res.write("<h3> Greetings " + customerName + "</h3>")
})

// don't match on req params within strings
app.get("/good-2", () => {
    return res.send({
      success: false,
      text: `User ${req.params.user_id} not found`,
    })
  })
  
  // don't match on custom req attributes
app.get("/good-3", () => {
    const userSettings = req.user.settings
    return res.send(userSettings)
  })