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
      secure: false,
      httpOnly: false,
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
    // Ok
      cookieSession({
        domain: "example.com",
        httpOnly: false,
        secure: true,
        name: "my-custom-cookie-name",
        maxAge: 24 * 60 * 60 * 1000,
        path: "/some-path",
      })
    )