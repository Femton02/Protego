import { cookieSession } from "cookie-session"

const session = require("express-session")
var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

let x = false;
let z = false;
{
  let y = false;
}

y = x || z;

y = false;

app.use(
  // bearer:expected javascript_express_cookie_missing_http_only
  session({
    cookie: {
      httpOnly: y,
    },
  })
)

app.use(
  // bearer:expected javascript_express_cookie_missing_http_only
  cookieSession({
    httpOnly: false,
  })
)

app.use(
  // bearer:expected javascript_express_cookie_missing_http_only
  cookieSession({
    httpOnly: true,
  })
)