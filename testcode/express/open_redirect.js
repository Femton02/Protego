module.exports.foo = function(req, res){
// expected vulnerability
    res.redirect(req.params.url)
// expected vulnerability
    res.redirect(req.query.url + "/bar")
// expected vulnerability
    res.redirect("https://" + req.params.url + "/bar")
// expected vulnerability
    res.redirect("http://" + req.params.path + "/bar")
}

module.exports.foo = function (_req, res) {
    res.redirect("https://google.com")
    res.redirect(!!req.query.google ? "https://google.com" : "https://bing.com")
    }