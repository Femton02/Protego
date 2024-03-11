function generateReport(matches, filePath) {
    console.log(`\nFile: ${filePath}`);
    if (matches.length === 0) {
        console.log("No vulnerabilities found.");
    } else {
        console.log("Vulnerabilities found:");
        matches.forEach((match, index) => {
            console.log(`#${index + 1}:`);
            console.log(`Rule: ${match.ruleName}`);
            console.log(`Description: ${match.description}`);
            console.log(`Location: Start ${match.location.start}, End ${match.location.end}`);
            console.log(`Line: ${match.line}`);
            console.log("------------");
        });
    }
}

module.exports = {
    generateReport
};
