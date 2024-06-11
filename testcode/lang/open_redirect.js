var myPath = new URLSearchParams(window.location)
var myPath2 = new URL(location.href)

// bearer:expected javascript_lang_open_redirect
window.location.href = myPath
// bearer:expected javascript_lang_open_redirect
location.href = myPath2

window.location.href = "https://mish.bearer.com/?" + params["userId"]
window.location.href = myPath ? ok : ok