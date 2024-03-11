const { readFileSync } = require('fs');
const { analyzeCodeWithLines } = require('./ruleEngine');
const { generateReport } = require('./reportEngine');

const filePaths = ['../test/test1.js', '../test/test2.js', '../test/test3.js'];

// Iterate over each file path
filePaths.forEach(filePath => {
    try {
        // Read the code from the file
        const code = readFileSync(filePath, 'utf-8');

        // Analyze the code
        const matches = analyzeCodeWithLines(code);

        // Generate report for the current file
        generateReport(matches, filePath);
    } catch (error) {
        console.error(`Error analyzing file "${filePath}":`, error);
    }
});
