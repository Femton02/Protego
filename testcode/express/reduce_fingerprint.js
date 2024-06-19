const express = require("express")
const helmet = require("helmet")
const cors = require("cors")

const app = express()

// expected vulnerability: reduce fingerprinting
app.disable("x-powered-by")

// expected vulnerability: reduce fingerprinting
app.use(helmet.hidePoweredBy())