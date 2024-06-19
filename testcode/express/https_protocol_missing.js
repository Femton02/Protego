// expected vulnerability
http.createServer(app).listen(port, () => {
    console.log("hello world");
  });

  https.createServer(httpsOptions, app).listen(port, () => {
    console.log("hello world");
  });