import { cookieSession } from "cookie-session"

const session = require("express-session")
var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

app.use(
  // expected vulnerability
  session({
    cookie: {
      domain: "example.com",
      httpOnly: false,
      secure: true,
      name: "my-custom-cookie-name",
      maxAge: 24 * 60 * 60 * 1000,
      path: "/some-path",
    },
  })
)

app.use(
  // expected vulnerability
  cookieSession({
    domain: "example.com",
    httpOnly: false,
    secure: false,
    name: "my-custom-cookie-name",
    maxAge: 24 * 60 * 60 * 1000,
    path: "/some-path",
  })
)

app.use(
  // ok
  cookieSession({
    domain: "example.com",
    httpOnly: true,
    secure: false,
    name: "my-custom-cookie-name",
    maxAge: 24 * 60 * 60 * 1000,
    path: "/some-path",
  })
)