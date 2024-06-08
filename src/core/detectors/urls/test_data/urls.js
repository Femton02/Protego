// Test Case 1: Simple String Assignment
let url1 = "https://example.com";

// Test Case 2: String Concatenation
let part1 = "https://";
let part2 = "example";
let part3 = ".com";
let url2 = part1 + part2 + part3;

// Test Case 3: Template Literals
let protocol = "https";
let domain = "example";
let tld = "com";
let url3 = `${protocol}://${domain}.${tld}`;

// Test Case 4: Complex Concatenation
let x = "api";
x = "api-new";
var y = "https://" + x + ".domain" + "ads";

// Test Case 5: Template Literals with Concatenation
let protocol2 = "https";
let domain2 = "example";
let path = "api";
let url4 = `${protocol2}://${domain2}/${path}`;

// Test Case 6: Function Call with Concatenation 
function getUrl(part1, part2, part3) {
    let z = part1 + part2;
    let y = z + part3;
    return y + "/functioncall";
}
let url5 = getUrl("https://", "example", ".com");

// Test Case 7: Base64 Encoding 
let encodedUrl = "aHR0cHM6Ly9leGFtcGxlLmNvbQ==";
let url6 = atob(encodedUrl);

// Test Case 8: Character Codes 
let url7 = String.fromCharCode(104, 116, 116, 112, 115, 58, 47, 47, 101, 120, 97, 109, 112, 108, 101, 46, 99, 111, 109);

// Test Case 9: Array Join
let parts = ["https://", "api-new", ".domain", "ads"];
let url8 = ["https://", "api-new", ".domain", "ads"].join('');
let url9 = parts.join('');

// Not detected yet
let url10 = Array(1).fill("https://").join('') + "api-new.domainads";