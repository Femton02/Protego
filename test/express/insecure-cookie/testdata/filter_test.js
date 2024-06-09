import { cookieSession } from "cookie-session"

const session = require("express-session")
var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())


app.use(
  // bearer:expected javascript_express_cookie_missing_http_only
  session({
    cookie: {
      httpOnly: false,
    },
  })
)

app.use(
  // bearer:expected javascript_express_cookie_missing_http_only
  cookieSession({
    httpOnly: 0,
  })
)

app.use(
  // bearer:expected javascript_express_cookie_missing_http_only
  cookieSession({
    httpOnly: true,
  })
)