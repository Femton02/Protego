const { readFileSync } = require('fs');
const { analyzeCode } = require('./ruleEngine');
const { generateReport } = require('./reportEngine');

const filePath = '../test/test1.js';
const code = readFileSync(filePath, 'utf-8');
const matches = analyzeCode(code);
generateReport(matches);
