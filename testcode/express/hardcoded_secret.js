import expressjwt from "expressjwt"
var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())
const jwt = expressjwt

app = express.app()

app.get(
  "/bad",
// expected vulnerability
  expressjwt({ secret: "my-hardcoded-secret" }),
  function (_req, res) {
    res.sendStatus(200)
  }
)

var secret = "my-hardcoded-secret"

// expected vulnerability
jwt.sign({ x: 42 }, secret, y)

// expected vulnerability
app.get("/bad-2", jwt({ secret: secret }), function (_req, res) {
  res.sendStatus(200)
})

// Ok
app.use(
  session({
    secret: config.secret,
    name: "my-custom-session-name",
  })
)