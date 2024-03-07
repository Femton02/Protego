// XSS (Cross-Site Scripting) Vulnerabilities
const userInputXSS_Vulnerable = "<script>alert('XSS');</script>";
document.getElementById('outputXSS_Vulnerable').innerHTML = userInputXSS_Vulnerable;

// Safe content for XSS
const userInputXSS_Safe = "Safe content";
document.getElementById('outputXSS_Safe').textContent = userInputXSS_Safe;

// SQL Injection Vulnerabilities
const userInputSQLInjection_Vulnerable = "'; DROP TABLE users; --";
const querySQLInjection_Vulnerable = "SELECT * FROM users WHERE username = '" + userInputSQLInjection_Vulnerable + "'";

// Safe SQL query
const userInputSQLSafe = "john";
const querySQLSafe = "SELECT * FROM users WHERE username = '" + userInputSQLSafe + "'";

// IDOR (Insecure Direct Object Reference) Vulnerabilities
const userIdIDOR_Vulnerable = 123;
const urlIDOR_Vulnerable = "https://example.com/api/user/" + userIdIDOR_Vulnerable;
fetch(urlIDOR_Vulnerable);

// Safe IDOR
const getCurrentUserId = () => 123; // Assuming a secure method to retrieve the user ID
const userIdIDOR_Safe = getCurrentUserId();
const urlIDOR_Safe = "https://example.com/api/user/" + userIdIDOR_Safe;
fetch(urlIDOR_Safe);

// More XSS (Cross-Site Scripting) Vulnerabilities
const userInputXSS_Vulnerable2 = "<img src='x' onerror='alert(\"XSS\")'>";
document.getElementById('outputXSS_Vulnerable2').innerHTML = userInputXSS_Vulnerable2;

// Safe content for XSS
const userInputXSS_Safe2 = "Safe content";
document.getElementById('outputXSS_Safe2').textContent = userInputXSS_Safe2;

// More SQL Injection Vulnerabilities
const userInputSQLInjection_Vulnerable2 = "' OR '1'='1";
const querySQLInjection_Vulnerable2 = "SELECT * FROM users WHERE username = '" + userInputSQLInjection_Vulnerable2 + "'";

// Safe SQL query
const userInputSQLSafe2 = "john";
const querySQLSafe2 = "SELECT * FROM users WHERE username = '" + userInputSQLSafe2 + "'";

// More IDOR (Insecure Direct Object Reference) Vulnerabilities
const userIdIDOR_Vulnerable2 = 456;
const urlIDOR_Vulnerable2 = "https://example.com/api/user/" + userIdIDOR_Vulnerable2;
fetch(urlIDOR_Vulnerable2);

// Safe IDOR
const userIdIDOR_Safe2 = getCurrentUserId(); // Assuming a secure method to retrieve the user ID
const urlIDOR_Safe2 = "https://example.com/api/user/" + userIdIDOR_Safe2;
fetch(urlIDOR_Safe2);
