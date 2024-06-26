var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())
var path = require("path")

app.get("/", function (req, res) {
  var file = req.params.file

// expected javascript_express_external_file_upload
  res.sendFile(file)
// expected javascript_express_external_file_upload
  res.sendFile(path.resolve(file))
// expected javascript_express_external_file_upload
  res.sendFile(req.params.file, {}, () => {})
// expected javascript_express_external_file_upload
  res.sendFile("file.txt", { root: path.join(__dirname, req.params.root) })
})

// Ok
app.get("/", function (_, res) {
    res.sendFile("index.js")
    res.sendFile(req.params.file, { root: path.join(__dirname, "public") })
  })