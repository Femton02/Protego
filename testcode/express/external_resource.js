var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

// expected vulnerability
app.get("/bad", (req, res) => {
  return res.render(req.query.path + "/results", { page: 1 })
})

app.get("/good", (_req, res) => {
    var internalPath = "/safe-resource"
    return res.render(internalPath + "/results", { page: res.params.page })
  })