const session = require("express-session")
const express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

// expected javascript_express_default_cookie_config
app.use(
  session({
    cookie: {},
  })
)

// expected javascript_express_default_cookie_config
app.use(
  session({
    cookie: {
      domain: "example.com",
      secure: true,
      httpOnly: false,
      maxAge: 24 * 60 * 60 * 1000,
      path: "/some-path",
    },
  })
)

// expected javascript_express_default_cookie_config
app.use(
  session({
    cookie: {
      domain: "example.com",
      secure: true,
      httpOnly: false,
      name: "my-custom-cookie-name",
    },
  })
)

// expected Ok
app.use(
    session({
      cookie: {
        domain: "example.com",
        secure: true,
        httpOnly: false,
        maxAge: 24 * 60 * 60 * 1000,
        path: "/some-path",
        name: "my-custom-cookie-name",
      },
    })
  )