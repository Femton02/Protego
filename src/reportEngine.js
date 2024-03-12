function generateReport(matches, filePath) {
    console.log('\x1b[36m%s\x1b[0m',`\nFile: ${filePath}`);
    if (matches.length === 0) {
        console.log('\x1b[32m%s\x1b[0m',"No vulnerabilities found.");
    } else {
        console.log('\x1b[31m%s\x1b[0m',"Vulnerabilities found:");
        matches.forEach((match, index) => {
            console.log('\x1b[36m%s\x1b[0m',`#${index + 1}:`);
            console.log('\x1b[31m%s\x1b[0m',`Rule: ${match.ruleName}`);
            console.log('\x1b[33m%s\x1b[0m',`Description: ${match.description}`);
            console.log('\x1b[33m%s\x1b[0m',`Location: Start ${match.location.start}, End ${match.location.end}`);
            console.log('\x1b[33m%s\x1b[0m',`Line: ${match.line}`);
            console.log("------------");
        });
    }
}

module.exports = {
    generateReport
};
