import expressjwt from "expressjwt"
const expjwt = require("expressjwt")
let exjwt = require("expressjwt")
var ejwt = require("expressjwt")
import * as expressjwt2 from "expressjwt"
const express = require("express")
var helmet = require("helmet")
let as = require("helmet")


var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())
// not detected yet
const jwt2 = expressjwt

app = express.app()

app.get(
  "/bad",
  // rule:expected javascript_express_hardcoded_secret
  expressjwt({ secret: "my-hardcoded-secret" }),
  // rule:expected javascript_express_hardcoded_secret
  expjwt({ secret: "my-hardcoded-secret" }),
  // rule:expected javascript_express_hardcoded_secret
  exjwt({ secret: "my-hardcoded-secret" }),
  // rule:expected javascript_express_hardcoded_secret
  ejwt({ secret: "my-hardcoded-secret" }),
  // rule:expected javascript_express_hardcoded_secret
  expressjwt2({ secret: "my-hardcoded-secret" }),

  // not detected as helmet doesn't have a secret option
  helmet({ secret: "my-hardcoded-secret" }),

  function (_req, res) {
    res.sendStatus(200)
  }
)

