var myPath = new URLSearchParams(window.location)
var myPath2 = new URL(location.href)

// expected vulnerability
window.location.href = myPath
// expected vulnerability
location.href = myPath2

window.location.href = "https://any.link.com/?" + params["userId"]
window.location.href = myPath ? ok : ok