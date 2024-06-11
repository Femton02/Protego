import axios from "axios"
var express = require("express")
var helmet = require("helmet")

var app = express()
app.use(helmet())
app.use(helmet.hidePoweredBy())

app.get("/inject", async (req, res) => {
// expected vulnerability
  axios.get(req.query.path).then((response) => res.json(response.data))
})

app.get("/inject", async (req, res) => {
// expected vulnerability
  response = await fetch("https://" + req.query.path)
  res.json(response.data)
})

app.get("/safety", async (_req, res) => {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await page.goto("https://any.link.com")
  
    res.send("success")
  })
  
  app.get("/safety-2", async (req, res) => {
    var token = req.user.tokens.find((token) => token.kind === "safe")
    axios.get(`https://mish.com/bears?access_token=${token.accessToken}`)
    axios.get("https://mish.com/bears?access_token=" + token.accessToken)
  
    res.send("success")
  })